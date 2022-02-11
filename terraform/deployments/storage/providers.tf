terraform {
  backend "azurerm" {
    storage_account_name = "lsaktfstate"
    resource_group_name  = "ls-tfstate-rg"
    container_name       = "function-app"
    key                  = "terraform.tfstate"
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.77.0"
    }
  }
}

provider "azurerm" {
  features {}
}