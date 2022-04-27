resource "mongodbatlas_alert_configuration" "main" {
  count = var.create_alert_configuration ? 1 : 0

  project_id = mongodbatlas_project.main.id
  event_type = var.alert_event_type
  enabled    = true

  notification {
    type_name     = var.alert_type_name
    interval_min  = var.alert_interval_min
    delay_min     = var.alert_delay_min
    sms_enabled   = var.alert_sms_enabled
    email_enabled = var.alert_email_enabled
    roles         = var.alert_roles
  }

  metric_threshold_config {
    metric_name = var.alert_metric_name
    operator    = var.alert_operator
    threshold   = var.alert_threshold
    units       = var.alert_units
    mode        = var.alert_mode
  }
}
