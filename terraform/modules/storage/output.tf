output "details" {
  value     = {
    account = {
      name = azurerm_storage_account.this.name
      primary_access_key = azurerm_storage_account.this.primary_blob_connection_string
    }
    container = {
      name = try(azurerm_storage_container.this[0].name, null)
    }
  }
  sensitive = true
}