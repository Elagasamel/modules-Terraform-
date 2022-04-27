# terraform-aws-alb-cloudwatch-logs-json

This Terraform module ships AWS ALB logs to CloudWatch Logs in JSON format.

## Requirements

* Terraform 0.12.x
* Python

## Example

```tf
resource "aws_cloudwatch_log_group" "test" {
  name              = aws_alb.test.name
  retention_in_days = 365
}

module "alb_logs_to_cloudwatch" {
  source  = "terraform-aws-alb-cloudwatch-logs-json"
  version = "1.0.0"

  bucket_name    = aws_s3_bucket.logs.bucket
  log_group_name = aws_cloudwatch_log_group.test.name

  create_alarm  = true
  alarm_actions = [aws_sns_topic.slack.arn]
  ok_actions    = [aws_sns_topic.slack.arn]
}

resource "aws_lambda_permission" "bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = module.alb_logs_to_cloudwatch.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.logs.arn
}

resource "aws_s3_bucket_notification" "logs" {
  bucket     = aws_s3_bucket.logs.bucket
  depends_on = ["aws_lambda_permission.bucket"]

  lambda_function {
    lambda_function_arn = module.alb_logs_to_cloudwatch.function_arn
    events              = ["s3:ObjectCreated:*"]
  }
}
```
