variable "python_version" {
  type        = string
  description = "The python version to use"
  default     = "3.9"
}

variable "storage" {
  sensitive = true
}

variable "rg" {}

variable "tags" {}

variable "function_app_name" {}

variable "app_settings" {
  sensitive = true
}

locals {
  function_app_name_no_hyphens = replace(var.function_app_name, "-", "")
  instrumentation_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.this.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.this.connection_string
    "APPLICATIONINSIGHTS_ROLE_NAME"         = var.function_app_name
  }
}
