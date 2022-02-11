variable "python_version" {
  type        = string
  description = "The python version to use"
  default     = "3.9"
}

variable "storage_account" {}

variable "rg" {}

variable "tags" {}

variable "function_app_name" {}

locals {
  function_app_name_no_hyphens = replace(var.function_app_name, "-", "")
}