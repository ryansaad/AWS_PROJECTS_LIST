# Deploying a 3-Tier WordPress Website on AWS

This repository provides a complete guide and resources for deploying a highly available, scalable, and secure WordPress website on AWS using a traditional 3-tier architecture.

## ☁️ Project Overview

This project walks through the manual setup of a production-ready cloud infrastructure. By separating the web, application, and database layers into distinct tiers, the architecture ensures security and resilience. The web tier is managed by an Application Load Balancer, the application tier consists of EC2 instances running WordPress in private subnets, and the database tier uses a managed Amazon RDS instance, also in a private subnet.


## ✨ Key Features

* **Secure Network Foundation**: A custom Virtual Private Cloud (VPC) with public and private subnets to isolate resources.
* **High Availability & Scalability**: An Application Load Balancer (ALB) distributes traffic across multiple EC2 instances in different Availability Zones.
* **Decoupled Application Layer**: WordPress application runs on EC2 instances within private subnets, shielded from direct internet access.
* **Managed & Persistent Storage**: Uses Amazon RDS for a managed MySQL database and Amazon EFS for a shared file system to store WordPress media and content, ensuring consistency across all instances.
* **Secure Outbound Connectivity**: NAT Gateways allow instances in private subnets to access the internet for updates without exposing them to inbound threats.


## 🛠️ Services Used

* **Networking**: Amazon VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway
* **Load Balancing**: Application Load Balancer (ALB)
* **Compute**: Amazon EC2
* **Database**: Amazon RDS (MySQL)
* **Shared Storage**: Amazon EFS (Elastic File System)
* **Security**: IAM Roles & Security Groups

## 🚀 Getting Started

To build this infrastructure, you will need an AWS account. The entire process is broken down into clear, manageable steps.

For the complete guide, please see the detailed instructions file

## 🧹 Clean-Up

To avoid ongoing AWS charges, a detailed clean-up guide is provided at the end of the [instructions file](INSTRUCTIONS.md) to help you tear down all created resources.
