variable "web_app_name" { ##This is a variable that sets the default name of the web application to "faceappdev".
  default = "faceappdev" ## The type of this variable is a string.
  type    = string
}

variable "web_app_settings_storage" { #This variable sets the default value of the storage option for the 
  default = false  ##web application to false. The type of this variable is a boolean.
  type    = bool
}

variable "web_app_settings_port" { ##  This variable sets the default value of the port that the web 
  default = 8000  ## application will listen on to 8000. The type of this variable is a number.
  type    = number
}

variable "web_app_start_time_limit" { ## This variable sets the default value of the start time limit for the 
  default = 20  ## web application to 20. The type of this variable is a number.
  type    = number
}

variable "webapp_service_plan_name" { ## This variable sets the default value of the name of the service plan 
  default = "faceapp-service-plan" ##for the web application to "faceapp-service-plan". The type of this variable is a string.
  type    = string
}

variable "webapp_os_type" { ## This variable sets the default value of the operating system type for the web application to "Linux". The type of this variable is a string.
  default = "Linux"
  type    = string
}

variable "webapp_sku_name" { ##  This variable sets the default value of the SKU name for the web application 
  default = "P1v2"    ## to "P1v2". The type of this variable is a string.
  type    = string
}

variable "docker_image_name" { ## This variable sets the default value of the name of the Docker image to "faceapp". The type of this variable is a string.
  default = "faceapp"
  type    = string
}

variable "docker_image_tag" { ## This variable sets the default value of the Docker image tag to "latest". 
  default = "latest"  ## The type of this variable is a string.
  type    = string
}
