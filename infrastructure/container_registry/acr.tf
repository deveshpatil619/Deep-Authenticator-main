##  Terraform configuration file that creates an Azure Container Registry (ACR) and outputs several values
# related to the ACR and the Azure resource group in which it is created.

module "resource_group" { ##  This line calls a Terraform module located in the "../resource_group" directory. 
  source = "../resource_group"  ##A Terraform module is a self-contained package of Terraform configurations 
} #that are managed as a group. The "resource_group" module is likely to create an Azure resource group, although its content is not shown in this code.

resource "random_id" "random_string_for_acr" { ##  This line creates a random string using the Terraform 
  byte_length = 8 ##"random_id" resource. The random string is used to generate a unique name for the ACR. 
} #The "byte_length" parameter sets the length of the random string to 8 bytes.

resource "azurerm_container_registry" "faceappacr" { ## This line creates an Azure Container Registry.
  name                = "${random_id.random_string_for_acr.dec}${var.faceapp_acr_name}" ## This line sets the name of the ACR. The name is created by concatenating the random string generated in step 2 and the value of the "faceapp_acr_name" Terraform variable.
  resource_group_name = module.resource_group.faceapp_resource_group_name ##This line sets the name of the Azure resource group in which the ACR will be created. The name is taken from the output of the "resource_group" module.
  location            = module.resource_group.faceapp_resource_group_location ## This line sets the location of the Azure resource group in which the ACR will be created. The location is taken from the output of the "resource_group" module.
  admin_enabled       = var.faceapp_acr_admin_enabled ##  This line sets the admin state of the ACR. The value is taken from the "faceapp_acr_admin_enabled" Terraform variable.
  sku                 = var.faceapp_acr_sku ## This line sets the SKU (pricing tier) of the ACR. The value is taken from the "faceapp_acr_sku" Terraform variable.
}

output "faceappacr_login_server" { ##  This line outputs the "login_server" value of the ACR. The "login_server" is the URL used to access the ACR.
  value = azurerm_container_registry.faceappacr.login_server  
}

output "faceappacr_admin_username" { # This line outputs the "admin_username" value of the ACR. The "admin_username" is the username used to authenticate to the ACR.
  value = azurerm_container_registry.faceappacr.admin_username
}

output "faceappacr_admin_password" { # This line outputs the "admin_password" value of the ACR. The "admin_password" is the password used to authenticate to the ACR
  value = azurerm_container_registry.faceappacr.admin_password
}

output "faceapp_resource_group_name" { ## This line outputs the name of the Azure resource group in which the ACR is created. The value is taken from the output of the "resource_group" module.
  value = module.resource_group.faceapp_resource_group_name
}

output "faceapp_resource_group_location" { ##  This line outputs the location of the Azure resource group in which the ACR
  value = module.resource_group.faceapp_resource_group_location
}







