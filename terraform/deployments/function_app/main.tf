resource "azurerm_resource_group" "rg" {
  name     = "rg-ls-func"
  location = "uksouth"
  tags     = local.tags
}

module "storage_account" {
  source  = "../../modules/storage"
  rg      = azurerm_resource_group.rg
  purpose = "func"
  tags    = local.tags
}

module "function_app" {
  source            = "../../modules/function"
  rg                = azurerm_resource_group.rg
  storage_account   = module.storage_account.details
  function_app_name = "func-price-alert-app"
  tags              = local.tags
}

