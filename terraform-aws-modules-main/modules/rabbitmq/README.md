<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_mq_broker.mq](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/mq_broker) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_auto_minor_version_upgrade"></a> [auto\_minor\_version\_upgrade](#input\_auto\_minor\_version\_upgrade) | n/a | `bool` | `true` | no |
| <a name="input_broker_name"></a> [broker\_name](#input\_broker\_name) | n/a | `string` | n/a | yes |
| <a name="input_deployment_mode"></a> [deployment\_mode](#input\_deployment\_mode) | n/a | `string` | `"CLUSTER_MULTI_AZ"` | no |
| <a name="input_engine_type"></a> [engine\_type](#input\_engine\_type) | n/a | `string` | `"RabbitMQ"` | no |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | n/a | `string` | `"3.8.11"` | no |
| <a name="input_host_instance_type"></a> [host\_instance\_type](#input\_host\_instance\_type) | n/a | `string` | `"mq.m5.large"` | no |
| <a name="input_mw_day_of_week"></a> [mw\_day\_of\_week](#input\_mw\_day\_of\_week) | n/a | `string` | `"SUNDAY"` | no |
| <a name="input_mw_time_of_day"></a> [mw\_time\_of\_day](#input\_mw\_time\_of\_day) | n/a | `string` | `"03:00"` | no |
| <a name="input_mw_time_zone"></a> [mw\_time\_zone](#input\_mw\_time\_zone) | n/a | `string` | `"UTC"` | no |
| <a name="input_password"></a> [password](#input\_password) | n/a | `string` | n/a | yes |
| <a name="input_publicly_accessible"></a> [publicly\_accessible](#input\_publicly\_accessible) | n/a | `bool` | `false` | no |
| <a name="input_security_groups"></a> [security\_groups](#input\_security\_groups) | n/a | `list(string)` | n/a | yes |
| <a name="input_storage_type"></a> [storage\_type](#input\_storage\_type) | n/a | `string` | `"ebs"` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | n/a | `any` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(any)` | `{}` | no |
| <a name="input_username"></a> [username](#input\_username) | n/a | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->