resource "aws_cognito_user_pool" "pool" {
  name = var.name

  alias_attributes           = var.alias_attributes
  auto_verified_attributes   = var.auto_verified_attributes
  email_verification_message = var.email_verification_message
  email_verification_subject = var.email_verification_subject
  mfa_configuration          = var.mfa_configuration
  sms_authentication_message = var.sms_authentication_message
  sms_verification_message   = var.sms_verification_message

  dynamic "sms_configuration" {
    for_each = (var.sms_configuration.external_id != "" && var.sms_configuration.sns_caller_arn != "") ? [1] : []

    content {
      external_id    = var.sms_configuration.external_id
      sns_caller_arn = var.sms_configuration.sns_caller_arn
    }
  }

  verification_message_template {
    email_message_by_link = var.verification_message_template.email_message_by_link
    email_subject_by_link = var.verification_message_template.email_subject_by_link
  }

  account_recovery_setting {
    dynamic "recovery_mechanism" {
      for_each = var.recovery_mechanism

      content {
        name     = recovery_mechanism.value.name
        priority = recovery_mechanism.value.priority
      }
    }
  }

  admin_create_user_config {
    allow_admin_create_user_only = false

    invite_message_template {
      email_message = var.invite_message_template.email_message
      email_subject = var.invite_message_template.email_subject
      sms_message   = var.invite_message_template.sms_message
    }
  }

  device_configuration {
    challenge_required_on_new_device      = var.challenge_required_on_new_device
    device_only_remembered_on_user_prompt = var.device_only_remembered_on_user_prompt
  }

  dynamic "lambda_config" {
    for_each = (var.lambda_config.kms_key_id != "" && var.lambda_config.custom_email_sender.lambda_arn != "" && var.lambda_config.custom_email_sender.lambda_version != "") ? [1] : []

    content {
      kms_key_id = var.lambda_config.kms_key_id

      custom_email_sender {
        lambda_arn     = var.lambda_config.custom_email_sender.lambda_arn
        lambda_version = var.lambda_config.custom_email_sender.lambda_version
      }
    }
  }

  dynamic "schema" {
    for_each = var.schema

    content {
      attribute_data_type      = schema.value.attribute_data_type
      developer_only_attribute = schema.value.developer_only_attribute
      mutable                  = schema.value.mutable
      name                     = schema.value.name
      required                 = schema.value.required

      string_attribute_constraints {
        max_length = schema.value.string_attribute_constraints.max_length
        min_length = schema.value.string_attribute_constraints.min_length
      }
    }
  }

  dynamic "software_token_mfa_configuration" {
    for_each = (var.software_token_mfa_configuration == true || var.software_token_mfa_configuration == false) ? [1] : []

    content {
      enabled = var.software_token_mfa_configuration
    }
  }

  dynamic "username_configuration" {
    for_each = (var.case_sensitive == true || var.case_sensitive == false) ? [1] : []

    content {
      case_sensitive = var.case_sensitive
    }
  }

  lifecycle {
    ignore_changes = [
      estimated_number_of_users
    ]
  }
}
