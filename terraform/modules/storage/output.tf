output "details" {
  value = {
    account = {
      name                      = azurerm_storage_account.this.name
      primary_connection_string = azurerm_storage_account.this.primary_connection_string
    }
    container = {
      name = try(azurerm_storage_container.this[0].name, null)
    }
  }
  sensitive = true
}