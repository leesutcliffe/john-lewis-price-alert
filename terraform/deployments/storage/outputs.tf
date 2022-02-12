output "storage" {
  value     = module.storage_account.details
  sensitive = true
}