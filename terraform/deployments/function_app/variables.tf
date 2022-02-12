locals {
  tags = {
    description = "testing function app"
    owner       = "lee.sutcliffe@armakuni.com"
  }
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "PYTHON_ENABLE_WORKER_EXTENSIONS" = "1"
    "CONTAINER_NAME" = data.terraform_remote_state.data.outputs.storage["container"]["name"]
    "STORAGE_CONNECTION" = data.terraform_remote_state.data.outputs.storage["account"]["primary_blob_connection_string"]
  }
}