## This is a Dockerfile, which is used to define the configuration for a Docker image. 
#The Docker image is then used to run a Docker container, which is a runtime instance of the image.

FROM python:3.8-slim-bullseye 
## This line specifies the base image to use as the starting point for the image being built. 
#In this case, the image is based on the official Python 3.8 image, with a slim version of the Debian-based Linux distribution "Bullseye".

WORKDIR /app
##  This line sets the working directory for any commands that follow in the Dockerfile. 
#The working directory is where all file operations will take place, such as copying files and running commands.
# In this case, the working directory is set to "/app".

COPY . /app
## This line copies the contents of the current directory (indicated by the dot) into the working 
# directory "/app". The contents of the current directory will be copied into the Docker image.

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && pip install -r requirements.txt
## This line runs a shell command to update the package information for the Debian-based system, install
# the ffmpeg, libsm6, and libxext6 packages, and then install the Python packages specified in the requirements.txt 
#file using pip.

CMD ["python", "app.py"]
## This line specifies the command to run when a container is started from the image. In this case, 
#the command is to run the python interpreter and pass it the argument app.py. This will start the Python script
# named app.py in the working directory "/app".