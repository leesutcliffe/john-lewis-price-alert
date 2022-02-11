resource "azurerm_storage_account" "this" {
  name                      = "ls${var.purpose}${random_string.this.result}"
  resource_group_name       = var.rg.name
  location                  = var.rg.location
  account_tier              = "Standard"
  account_kind              = "Storage"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"
  tags                      = var.tags
}

resource "random_string" "this" {
  length = 5
  number = true
  lower = false
  special = false
  upper = false
}

resource "azurerm_storage_container" "this" {
  count = var.container != "" ? 1 : 0
  name                  = var.container
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = "private"
}