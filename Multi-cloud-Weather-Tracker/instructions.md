# ⚙️ Project Deployment Instructions

This guide provides the detailed steps to deploy the Multi-Cloud Weather Tracker project from scratch. This project involves a mix of automated **Terraform** steps and **manual setup** for services like domain registration and SSL.

---

## 1. Prerequisites

Before you begin, you must have the following:

1.  **A Purchased Domain Name:** This project assumes you own a domain (e.g., `rsdeveloper.shop`) from a registrar like **Namecheap**.
2.  **AWS Account:** An active AWS account with permissions to manage Route 53, S3, CloudFront, ACM, and IAM.
3.  **Azure Account:** An active Azure subscription (a free trial works).
4.  **Software:**
    * [Terraform](https://www.terraform.io/downloads) installed locally.
    * [AWS CLI](https://aws.amazon.com/cli/) installed and configured (`aws configure`).
    * [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed (`az login`).
5.  **Project Files:** The `website` folder containing the static app files must be in the root of your repository.

---

## 2. Initial Setup & Credentials

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create Credential Files:**
    Terraform needs API keys to provision resources. We will create two files to hold these keys. **These files should be listed in your `.gitignore` and NEVER be pushed to GitHub.**

    * Create `aws_credentials.tfvars`:
        ```tfvars
        aws_access_key = "YOUR_AWS_ACCESS_KEY"
        aws_secret_key = "YOUR_AWS_SECRET_KEY"
        ```

    * Create `azure_credentials.tfvars`:
        ```tfvars
        azure_client_id       = "YOUR_AZURE_APP_ID"
        azure_client_secret   = "YOUR_AZURE_PASSWORD"
        azure_subscription_id = "YOUR_AZURE_SUBSCRIPTION_ID"
        azure_tenant_id       = "YOUR_AZURE_TENANT_ID"
        ```
    *(To get your Azure credentials, run `az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/YOUR_SUBSCRIPTION_ID"`)*

---

## 3. Manual AWS Setup (The "Click-Ops" Part)

These steps **must** be done manually *before* running Terraform, as Terraform needs the outputs from these services.

1.  **Create Route 53 Hosted Zone:**
    * Go to the **AWS Route 53** console.
    * Create a **Public Hosted Zone** for your domain (e.g., `rsdeveloper.shop`).
    * After it's created, copy the four nameservers (NS record).

2.  **Update Domain Nameservers:**
    * Go to your domain registrar (e.g., **Namecheap**).
    * Find your domain and change the nameservers from "Basic DNS" to "Custom DNS".
    * Paste the four Route 53 nameservers.
    * **Wait 30-60 minutes** for this to propagate. This is essential for the next step.

3.  **Request SSL Certificate (in `us-east-1`):**
    * Go to the **AWS Certificate Manager (ACM)** console.
    * **In the top-right, change your region to `us-east-1` (N. Virginia).** This is a *requirement* for CloudFront.
    * Request a **public certificate**.
    * Add your domain names: `rsdeveloper.shop` and `*.rsdeveloper.shop` (or `www.rsdeveloper.shop`).
    * Choose **DNS Validation**.
    * Click "Create records in Route 53". This will automatically validate your certificate.
    * Wait until the certificate status is **"Issued"**.

4.  **Create CloudFront Distribution:**
    * Go to the **AWS CloudFront** console.
    * Click **"Create distribution"**.
    * **Origin domain:** Select your S3 bucket (e.g., `weather-tracker-app-bucket-3453821...`).
    * **S3 bucket access:** Select **"Yes use OAC"** (Origin Access Control) and click "Create new OAC".
    * **Default root object:** Enter `index.html`.
    * **Alternate domain names (CNAMEs):** Add `rsdeveloper.shop` and `www.rsdeveloper.shop`.
    * **Custom SSL certificate:** Select your newly "Issued" ACM certificate.
    * Create the distribution. This will take 10-15 minutes.
    * Once deployed, **copy the CloudFront "Domain name"** (e.g., `d1dql0l5xpl9jn.cloudfront.net`).

---

## 4. Terraform Deployment

Now that you have your CloudFront domain name, you can deploy the full infrastructure.

1.  **Update `main.tf`:**
    * Open your `main.tf` file.
    * Find all `aws_route53_record` and `aws_route53_health_check` resources.
    * Paste your CloudFront domain name (e.g., `d1dql0l5xpl9jn.cloudfront.net`) into the `fqdn`, `name`, or `records` fields where indicated.
    * Ensure your `main.tf` file matches the final version from our discussion (with the `failover.` subdomain logic).

2.  **Initialize and Apply Terraform:**
    * Run `terraform init` to download the providers.
    * Run the final apply command:
        ```bash
        terraform apply -var-file="aws_credentials.tfvars" -var-file="azure_credentials.tfvars"
        ```
    * Terraform will show you a plan. Type `yes` to deploy. This will create your S3 bucket, upload all files, create the Azure storage, and set up all Route 53 health checks and DNS records.

---

## 5. Final S3 Bucket Policy (Troubleshooting)

The `terraform apply` may fail, or your site may show "Access Denied." This is because the CloudFront OAC requires a specific bucket policy.

1.  **Go to the S3 Console** and click your bucket (`weather-tracker-app-bucket-3453821`).
2.  Go to the **Permissions** tab and click **Edit** on the **Bucket policy**.
3.  If it is blank, paste in the following policy. This allows your specific CloudFront distribution to access your S3 bucket.

    *(Note: You must replace `861276082757` with your AWS Account ID and `E3GD4H4GEJE7XE` with your CloudFront Distribution ID).*

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowCloudFrontServicePrincipalReadOnly",
          "Effect": "Allow",
          "Principal": {
            "Service": "cloudfront.amazonaws.com"
          },
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::weather-tracker-app-bucket-3453821/*",
          "Condition": {
            "StringEquals": {
              "AWS:SourceArn": "arn:aws:cloudfront::861276082757:distribution/E3GD4H4GEJE7XE"
            }
          }
        }
      ]
    }
    ```
4.  Save the policy.

---

## 6. Verification & Testing

After waiting ~30 minutes for DNS to propagate:

* **Main Site:** `https://rsdeveloper.shop` and `https://www.rsdeveloper.shop` should be accessible.
* **Failover Site:** `http://failover.rsdeveloper.shop` should be accessible.
* **Test the Failover:** Go to the CloudFront console, **disable** your distribution, and wait 10-15 minutes. `failover.rsdeveloper.shop` should now serve the site from Azure.

---

## 7. Clean-Up

To avoid ongoing costs, destroy all resources when you are finished.

```bash
terraform destroy -var-file="aws_credentials.tfvars" -var-file="azure_credentials.tfvars"
```
