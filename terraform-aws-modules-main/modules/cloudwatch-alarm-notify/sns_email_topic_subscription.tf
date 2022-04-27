# Create sns topic for email notifications (should share same region with provider)
resource "aws_sns_topic" "k8s-alerts-notify-email" {
  name = "${replace(var.alarm_name, ".", "-")}-email"

  delivery_policy = <<EOF
{
  "http": {
    "defaultHealthyRetryPolicy": {
      "minDelayTarget": 20,
      "maxDelayTarget": 20,
      "numRetries": 3,
      "numMaxDelayRetries": 0,
      "numNoDelayRetries": 0,
      "numMinDelayRetries": 0,
      "backoffFunction": "linear"
    },
    "disableSubscriptionOverrides": false,
    "defaultThrottlePolicy": {
      "maxReceivesPerSecond": 1
    }
  }
}
EOF

}

# Subscribe sns to email
resource "aws_sns_topic_subscription" "email" {
  count     = length(var.sns_subscription_email_address_list)
  topic_arn = aws_sns_topic.k8s-alerts-notify-email.arn
  protocol  = "email"
  endpoint  = element(var.sns_subscription_email_address_list, count.index)
}
