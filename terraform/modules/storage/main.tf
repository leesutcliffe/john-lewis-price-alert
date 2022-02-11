resource "azurerm_storage_account" "this" {
  name                      = "ls${var.purpose}${random_integer.this.result}"
  resource_group_name       = var.rg.name
  location                  = var.rg.location
  account_tier              = "Standard"
  account_kind              = "Storage"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"
  tags                      = var.tags
}

resource "random_integer" "this" {
  max = 9
  min = 6
}