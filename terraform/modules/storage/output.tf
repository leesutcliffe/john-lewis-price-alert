output "details" {
  value = {
    account = {
      name                      = azurerm_storage_account.this.name
      primary_connection_string = azurerm_storage_account.this.primary_connection_string
      primary_access_key        = azurerm_storage_account.this.primary_access_key
    }
    container = {
      name = try(azurerm_storage_container.this[0].name, null)
    }
  }
  sensitive = true
}