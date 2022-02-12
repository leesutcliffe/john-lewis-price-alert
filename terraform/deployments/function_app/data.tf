data "terraform_remote_state" "data" {
  backend = "azurerm"
  config = {
    storage_account_name = "lsaktfstate"
    resource_group_name  = "ls-tfstate-rg"
    container_name       = "function-app"
    key                  = "terraform.tfstate"
  }
}