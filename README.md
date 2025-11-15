# 🌩️ Multi-Cloud Weather Tracker with DNS Failover

This project demonstrates a highly-available, multi-cloud static website deployed on both **AWS** and **Azure**, with automated DNS-based disaster recovery managed by **Terraform** and **AWS Route 53**.

The application itself is a simple weather tracker, but the focus of the project is the resilient infrastructure it runs on. If the primary site on AWS goes down, Route 53 health checks will automatically fail over and redirect all traffic to the secondary site hosted on Azure.



---

## 🏛️ Architecture & Key Features

* **Infrastructure as Code (IaC):** The entire infrastructure (for both clouds) is defined and managed using **Terraform**, allowing for repeatable, automated, and version-controlled deployments.
* **Primary Site (AWS):**
    * **Amazon S3:** Hosts the static website (HTML, CSS, JS).
    * **Amazon CloudFront:** Acts as the global CDN, providing low-latency content delivery, HTTPS/SSL, and security (via OAC).
    * **Amazon Route 53:** Manages the custom domain (`rsdeveloper.shop`) and performs active health checks.
    * **AWS Certificate Manager (ACM):** Provides the free, auto-renewing SSL certificate for the custom domain.
* **Secondary/Failover Site (Azure):**
    * **Azure Blob Storage:** Hosts a mirrored copy of the static website, configured for static site hosting.
    * **Azure Resource Group:** Organizes all related Azure assets.
* **DNS Failover:**
    * Route 53 health checks constantly monitor the primary AWS endpoint.
    * If the primary health check fails, Route 53's failover routing policy automatically reroutes traffic to the secondary Azure endpoint.
    * *Note: Due to DNS rules (CNAME vs. A records), the root (`rsdeveloper.shop`) and `www` subdomains point to the primary site, while the failover demonstration is implemented on the `failover.rsdeveloper.shop` subdomain.*

---

## 🛠️ Services Used

### AWS
* Amazon S3
* Amazon CloudFront
* Amazon Route 53
* AWS Certificate Manager (ACM)
* AWS IAM (for OAC)

### Azure
* Azure Blob Storage
* Azure Storage Account
* Azure Resource Group

### DevOps
* Terraform
* GitHub

---

## 🚀 How to Run

Detailed, step-by-step instructions for deploying this project are available in the `instructions.md` file.

[**See the full setup instructions here](./instructions.md)**](https://github.com/ryansaad/Multi-cloud-Weather-Tracker
/blob/main/instructions.md)

