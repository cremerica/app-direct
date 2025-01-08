# AppDirect README

AppDirect is a sample Python Flask application used to test various technologies. This application is meant to be containerized and run in a Kubernetes Pod. The *yaml* directory contains a simple deployment yaml.

The application provides output to stdout and can be obtained via `kubectl logs <pod name>` if running in Kubernetes. This is the standard flask output.

This repository also includes a Github Action workflow to deploy to an EC2 instance for testing. Have fun!!!!!


