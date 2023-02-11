## The code block defines three Terraform variables: faceapp_acr_name, faceapp_acr_sku, and faceapp_acr_admin_enabled.

variable "faceapp_acr_name" { ## faceapp_acr_name has a default value of "faceappACR" and a data type of string.
  default = "faceappACR"
  type    = string
}

variable "faceapp_acr_sku" { ## faceapp_acr_sku has a default value of "Standard" and a data type of string.
  default = "Standard"
  type    = string
}

variable "faceapp_acr_admin_enabled" { ## faceapp_acr_admin_enabled has a default value of true and a data type of boolean.
  default = true
  type    = bool
}
