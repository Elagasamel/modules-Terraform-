# How to
1. assign your widgets to the widgets variable, but don't insert any "", so the right syntax is:
   widgets = {
    "widgets": [ ....
      ...
    ]
   }
2. run

```
module "cloudwatch" {
  source = "git::https://github.com/dasmeta/terraform.git//modules/cloudwatch?ref="

  dashboard_name = "cloudwatch dashboard name"
  widgets = "some json file"
}
```
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
| [aws_cloudwatch_dashboard.applications](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_dashboard) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_dashboard_name"></a> [dashboard\_name](#input\_dashboard\_name) | Cloudwatch dashboard name | `string` | `"newdashboard"` | no |
| <a name="input_widgets"></a> [widgets](#input\_widgets) | Cloudwatch widgets | `any` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->