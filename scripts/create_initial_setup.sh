#!bin/bash
## This is a shell script written in the Bash language, and it's used to create resources in Microsoft Azure.
##This script is using the Azure CLI, a command-line tool for managing Azure resources, to create a resource group,
#a storage account, and a storage container in the "eastus2" location. The purpose of these resources is not specified in the script.

# Here's a detailed explanation of each command:

az group create -n 619faceauthtfstate -l eastus2 ## This command creates a new Azure resource group.
# The -n option specifies the name of the resource group, which is "619faceauthtfstate", and the -l option specifies the location, which is "eastus2".
 
az storage account create -n 619faceauthtfstate -g 619faceauthtfstate -l eastus2 --sku "Standard_LRS"  ## This command creates
# a new Azure storage account. The -n option specifies the name of the storage account, which is
# "619faceauthtfstate", the -g option specifies the name of the resource group, which is "619faceauthtfstate", 
#and the -l option specifies the location, which is "eastus2". The --sku option specifies the storage account SKU, which is "Standard_LRS".
 
az storage container create -n tfstate --account-name 619faceauthtfstate ##  This command creates a new Azure storage 
#container. The -n option specifies the name of the container, which is "tfstate". The --account-name option 
#specifies the name of the storage account, which is "619faceauthtfstate".
