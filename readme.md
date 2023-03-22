# AppDirect Readme

AppDirect is a sample Python Flask application used to test various technologies. This application is meant to be containerized and run in a Kubernetes Pod. The *yaml* directory contains a simple deployment yaml.

The application provides output to stdout and can be obtained via `kubectl logs <pod name>` if running in Kubernetes. 

Files of note in this directory:

* **Dockerfile:** This file is used to containerize AppDirect as 'cremerfc/appdirect'
* **Jenkinsfile:** This file does an scm checkout on the repository and builds the container, pushes it Docker Hub using the build number and 'latest' as the image tag. It then creates a new release version in Replicated.
* **Requirements.txt** this file is the result of running `pip freeze > Requirements.txt`, and contains a list of all of the Python dependencies and versions needed by AppDirect. This file is used in the container building process to install all needed Python dependencies.

This repository also includes a Github Action workflow to deploy to an EC2 instance for testing. Have fun!
