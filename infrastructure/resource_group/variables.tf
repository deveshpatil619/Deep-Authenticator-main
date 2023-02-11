##  Terraform configuration file that defines two Terraform variables: faceapp_resource_group_name and faceapp_resource_group_location.

variable "faceapp_resource_group_name" { ## This line declares a Terraform variable with the name "faceapp_resource_group_name".
  type    = string ## This line sets the type of the variable to "string". In Terraform, variables can have different types such as string, number, list, etc.
  default = "faceappRG" ## This line sets a default value for the variable. In this case, the default value is "faceappRG".
}

variable "faceapp_resource_group_location" { ## This line declares another Terraform variable with the name "faceapp_resource_group_location"
  type    = string ##  This line sets the type of the variable to "string".
  default = "eastus" ## This line sets a default value for the variable. In this case, the default value is "eastus".
}