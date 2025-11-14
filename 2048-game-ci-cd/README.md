# CI/CD Pipeline for a 2048 Game on AWS

This repository contains the code and instructions for building and deploying a complete CI/CD pipeline for a containerized 2048 web game on Amazon Web Services.
The pipeline automates the entire process of building a Docker image from source, pushing it to a container registry, and deploying it to a scalable, serverless infrastructure on AWS.

***

## ☁️ Project Overview

This project demonstrates a real-world DevOps workflow. When a developer pushes a code change to this GitHub repository, AWS CodePipeline automatically triggers a new build. AWS CodeBuild creates a new Docker container image, which is then stored in Amazon ECR. Finally, CodePipeline deploys this new image to an Amazon ECS cluster running on AWS Fargate, making the change live with zero manual intervention.

### Architectural Diagram


### Final Result


***

## 🛠️ Services & Technologies Used

* **AWS CodePipeline**: The core CI/CD orchestration service that automates the release workflow.
* **AWS CodeBuild**: A fully managed build service that compiles source code, runs tests, and produces software packages (in this case, a Docker image).
* **Amazon ECR (Elastic Container Registry)**: A secure, scalable, and reliable AWS-managed container image registry service.
* **Amazon ECS (Elastic Container Service)**: A highly scalable, high-performance container orchestration service that supports Docker containers.
* **AWS Fargate**: A serverless compute engine for containers that removes the need to provision and manage servers.
* **IAM Roles & Policies**: For providing secure, granular permissions between AWS services.
* **Docker**: For containerizing the 2048 application.
* **GitHub**: As the source code repository.

***

To replicate this project, you will need to have Docker and the AWS CLI installed and configured on your local machine.

For a complete, step-by-step guide on how to set up the infrastructure and deploy the pipeline, please see the instructions file:

## Note: AWS services charges to avoid.

## 🧹 Clean-Up

To avoid ongoing charges, remember to delete all the AWS resources created during this project. Detailed clean-up steps are provided at the end of the intructions.md file
