import csv
import gzip
import json
from datetime import datetime
from os import environ
from queue import Full
from tempfile import NamedTemporaryFile
from urllib.parse import unquote_plus

import boto3

LOG_GROUP_NAME = environ["LOG_GROUP_NAME"]


# https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
FIELD_NAMES = [
    "type",
    "timestamp",
    "elb",
    "client:port",
    "target:port",
    "request_processing_time",
    "target_processing_time",
    "response_processing_time",
    "elb_status_code",
    "target_status_code",
    "received_bytes",
    "sent_bytes",
    "request",
    "user_agent",
    "ssl_cipher",
    "ssl_protocol",
    "target_group_arn",
    "trace_id",
    "domain_name",
    "chosen_cert_arn",
    "matched_rule_priority",
    "request_creation_time",
    "actions_executed",
    "redirect_url",
    "error_reason",
    "target:port_list",
    "target_status_code_list",
]

logs_client = boto3.client("logs")
s3_client = boto3.client("s3")


class LogEventsBatch:
    """
    Stores multiple log events to be sent in a batch to CloudWatch.

    This is used to track the limits of the PutLogEvents API call:
        * number of log events
        * combined size of messages

    """

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_log_events
    MAX_BATCH_COUNT = 10000
    MAX_BATCH_SIZE = 1048576
    LOG_EVENT_OVERHEAD = 26

    def __init__(self):
        self._events = []
        self._size = 0

    def read(self):
        """
        Returns the log events in this batch,
        and clears it out.

        """

        try:
            return self._events
        finally:
            self._events = []
            self._size = 0

    def write(self, message, timestamp):
        """
        Adds a log event to the batch. If the log event cannot be added
        due to batch limits, then a Full exception is raised instead.

        """

        if len(self._events) >= self.MAX_BATCH_COUNT:
            raise Full

        event_size = len(message) + self.LOG_EVENT_OVERHEAD
        if self._size + event_size > self.MAX_BATCH_SIZE:
            raise Full

        event = {"message": message, "timestamp": timestamp}

        self._events.append(event)
        self._size += event_size


class LogStream:
    def __init__(self, name):
        self._name = name
        self._log_events_batch = LogEventsBatch()
        self._sequence_token_kwarg = {}

    def flush(self):
        """
        Sends the current log events batch to CloudWatch
        and then clears the batch.

        """

        events = self._log_events_batch.read()

        if not events:
            return

        response = logs_client.put_log_events(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=self._name,
            logEvents=events,
            **self._sequence_token_kwarg,
        )

        self._sequence_token_kwarg["sequenceToken"] = response["nextSequenceToken"]

        rejected_info = response.get("rejectedLogEventsInfo")
        if rejected_info:

            # The expired log events.
            expired_index = rejected_info.get("expiredLogEventEndIndex")
            if expired_index is not None:
                expired_events = events[0:expired_index]
                for event in expired_events:
                    print("ERROR: CloudWatch Log event expired: {}".format(event))

            # The log events that are too old.
            too_old_index = rejected_info.get("tooOldLogEventEndIndex")
            if too_old_index is not None:
                too_old_events = events[0:too_old_index]
                for event in too_old_events:
                    print(
                        "ERROR: CloudWatch Log event timestamp too old: {}".format(
                            event
                        )
                    )

            # The log events that are too new.
            too_new_index = rejected_info.get("tooNewLogEventStartIndex")
            if too_new_index is not None:
                too_new_events = events[too_new_index:-1]
                for event in too_new_events:
                    print(
                        "ERROR: CloudWatch Log event timestamp too new: {}".format(
                            event
                        )
                    )

            raise Exception(rejected_info)

    def truncate(self):
        """
        Ensures that the log stream exists in CloudWatch.
        Any existing logs in the log stream will be deleted.

        """

        try:
            logs_client.create_log_stream(
                logGroupName=LOG_GROUP_NAME, logStreamName=self._name
            )
        except logs_client.exceptions.ResourceAlreadyExistsException:
            logs_client.delete_log_stream(
                logGroupName=LOG_GROUP_NAME, logStreamName=self._name
            )
            logs_client.create_log_stream(
                logGroupName=LOG_GROUP_NAME, logStreamName=self._name
            )

        self._sequence_token_kwarg.clear()

    def write(self, message, timestamp):
        """
        Adds a log event to the batch. If the log event cannot be added
        due to batch limits, then a Full exception is raised instead.

        This only prepares the batch of log events to be sent to CloudWatch.
        Use flush() to send the log event batch to CloudWatch.

        """

        self._log_events_batch.write(message, timestamp)


def parse_iso8601(string):
    """
    Parses a string such as 2020-01-15T12:29:59.432228Z
    and returns a matching datetime object.

    """

    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")


def read_log_entries(bucket, key):
    """
    Reads ALB log entries from an S3 object.
    Generates a dictionary for each log line.

    """

    with NamedTemporaryFile() as temp_file:
        s3_client.download_file(bucket, key, temp_file.name)
        with gzip.open(temp_file.name, mode="rt") as extracted_file:
            reader = csv.DictReader(
                extracted_file, fieldnames=FIELD_NAMES, delimiter=" "
            )
            yield from reader


def handler(event, context):
    for record in event["Records"]:

        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        print(f"Processing s3://{bucket}/{key}")

        log_stream = LogStream(f"{bucket}/{key}")
        log_stream.truncate()

        # Logs must be added to CloudWatch in chronological order.
        # Entries in the S3 log file are sometimes out of order.
        # So create a list with every log entry and sort them
        # before pushing them to CloudWatch.

        parsed_entries = []
        for entry in read_log_entries(bucket, key):
            message = json.dumps(entry)
            timestamp = int(parse_iso8601(entry["timestamp"]).timestamp() * 1000)
            parsed_entries.append((timestamp, message))

        parsed_entries.sort()

        for (timestamp, message) in parsed_entries:
            try:
                log_stream.write(message, timestamp)
            except Full:
                log_stream.flush()
                log_stream.write(message, timestamp)

        log_stream.flush()
