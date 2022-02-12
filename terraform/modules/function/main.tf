

resource "azurerm_function_app" "this" {
  name                = var.function_app_name
  location            = var.rg.location
  resource_group_name = var.rg.name

  app_service_plan_id        = azurerm_app_service_plan.this.id
  storage_account_name       = var.storage.account.name
  storage_account_access_key = var.storage.account.primary_access_key
  https_only                 = true
  os_type                    = "linux"
  version                    = "~3"

  identity {
    type = "SystemAssigned"
  }

  site_config {
    http2_enabled    = true
    app_scale_limit  = 1
    linux_fx_version = "PYTHON|${var.python_version}"
  }

  auth_settings {
    enabled = false
  }

  app_settings = var.app_settings

  lifecycle {
    ignore_changes = [
      app_settings
    ]
  }
  tags = var.tags
}

resource "azurerm_app_service_plan" "this" {
  name                = replace(local.function_app_name_no_hyphens, "func", "plan")
  resource_group_name = var.rg.name
  location            = var.rg.location
  reserved            = true
  kind                = "FunctionApp"

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
  tags = var.tags
}
