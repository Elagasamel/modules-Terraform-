variable "alb_name" {
  type        = string
  description = "Ingress name"
}

variable "hostname" {
  type        = string
  description = "Hostname"
}

variable "annotations" {
  type    = any
  default = {}
}

variable "path" {
  type = list(object({
    service_name = string
    service_port = string
    path         = string
  }))
  default = []
}
variable "default_backend" {
  type = object({
    service_name = string
    service_port = string
  })
}
# TODO: check if there is way to get this data as kubernetes data
variable "api_version" {
  type        = string
  default     = "networking/v1"
  description = "The api version of ingress, can be networking/v1 and extensions/v1beta1 for now"
}

variable "namespace" {
  type    = string
  default = "default"
}
