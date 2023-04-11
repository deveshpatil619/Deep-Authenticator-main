## This Terraform code sets up the backend for Terraform state management and defines the Azure provider.



terraform { ## This block specifies the backend for Terraform state management. In this case, it is using Azure backend and the state will be stored in an Azure storage account.
  backend "azurerm" { ## This block provides the configuration details for the Azure backend. 
  #It specifies the resource group name, storage account name, container name, and key for the Terraform state file
    resource_group_name  = "619faceauthtfstate"
    storage_account_name = "619faceauthtfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" { ##  This block sets up the Azure provider. The features {} block is empty,
  features {} ## indicating that no specific features are enabled for the provider.
}

module "web_app" { ## his block declares a Terraform module named "web_app"
  source = "./web_app" ## and specifies the source for the module as the "./web_app" directory.
}


