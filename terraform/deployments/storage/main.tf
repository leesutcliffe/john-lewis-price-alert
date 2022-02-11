resource "azurerm_resource_group" "rg" {
  name     = "rg-ls-data"
  location = "uksouth"
  tags     = local.tags
}

module "storage_account" {
  source  = "../../modules/storage"
  purpose = "data"
  rg      = azurerm_resource_group.rg
  tags    = local.tags
}