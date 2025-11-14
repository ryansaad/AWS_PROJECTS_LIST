# Step-by-Step Project Instructions

## 1. Prerequisites: Docker & AWS CLI

Before you begin, ensure you have **Docker** and the **AWS CLI** installed and configured on your system.

### Install Docker
Follow the official instructions for your operating system:
- [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker for macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Docker for Linux](https://docs.docker.com/engine/install/ubuntu/)

Verify the installation:
docker --version


## 2. Install and Configure AWS CLI
Follow the official guide to install the AWS CLI.
Configure the CLI with your AWS credentials. You'll need an Access Key ID and a Secret Access Key from an IAM user with appropriate permissions (e.g., AdministratorAccess for this project).


## 3. Prepare the 2048 Game Code
### Step 1: Clone the Source Code
Clone the initial project files to your local machine.


git clone repository_URL_HERE

### Step 2 Create Your Own GitHub Repository
Go to GitHub and create a new, empty public repository (e.g., 2048-aws-pipeline).

* Note: Do not initialize it with a README or .gitignore file.
* Copy the new repository's URL (e.g., https://github.com/your-username/2048-aws-pipeline.git).

### Step 3: Modify buildspec.yml
* This file tells AWS CodeBuild how to build your project. Update the placeholder values.
- This file is provided in the repository.

 - IMPORTANT: Replace <your-region> and <your-ecr-repository-uri
 - IMPORTANT: Replace <your-ecr-repository-uri>
 - IMPORTANT: Replace <container-name>, <your-ecr-repository-uri>, and <repository-name>

### Step 4: Push Code to Your Repository
- Now, push the game code to your new GitHub repository.

- git init
- Remove the old remote origin and add yours
- git remote remove origin
- git remote add origin <your-repository-url> # Paste your URL here
 
- Add, commit, and push the code
- git add .
- git commit -m "Initial commit of 2048 game source"
- git branch -M main
- git push -u origin main


## 4. Manually Deploy to AWS (First Time)
We will deploy the container manually once to ensure it works and to create the necessary AWS resources like the cluster and service.

### Step 1: Create ECR Repository
- Go to the Amazon ECR console.
- Click Create repository.
- Set Visibility to Private.
- Enter a Repository name (e.g., 2048-game-repo).
- Click Create repository.
- Copy the repository URI. You will need this for your buildspec.yml and the commands below.

### Step 2: Build and Push Docker Image Manually

Replace <ECR_URI> with the URI you just copied

- Build the image

- docker build -t 2048-game .

- Tag the image for ECR
- docker tag 2048-game:latest <ECR_URI>:latest

- Login to ECR
- Replace <region> and <ECR_URI>
- aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ECR_URI>

- Push the image
- docker push <ECR_URI>:latest
- Verify the image appears in your ECR repository.

### Step 3: Create an ECS Cluster
- Go to the Amazon ECS console.
- Click Clusters -> Create cluster.
- Name the cluster (e.g., 2048-game-cluster).
- For Infrastructure, select AWS Fargate (Serverless).
- Click Create.

### Step 4: Create an ECS Task Definition
In the ECS console, go to Task Definitions -> Create new Task Definition.
- Give it a name (e.g., 2048-game-task).
- Under Container details, enter:
- Container name: 2048-container
- Image URI: Your <ECR_URI>:latest
- Port mappings: 80
- Leave other settings as default and click Create.

### Step 5: Create an ECS Service
- Navigate to your cluster -> Services tab -> Create.
- Launch type: FARGATE.
- Task Definition: Select 2048-game-task.
- Service name: 2048-service.
- Number of tasks: 1.
- Under Networking, select a VPC and subnets. Crucially, enable "Public IP".
- Create or select a Security Group that allows inbound HTTP traffic on port 80.
- Click Create.

- Wait for the task to be in the RUNNING state. Click on the task, and under the Network section, find the Public IP. You should be able to access the game by pasting this IP into your browser.

## 5. Set Up the CI/CD Pipeline
### Step 1: Create IAM Role for CodeBuild
- Go to the IAM console -> Roles -> Create role.
- Trusted entity type: AWS service.
- Use case: CodeBuild. Click Next.
- Attach the following managed policies:
1. AmazonEC2ContainerRegistryFullAccess
2. AWSCodeBuildDeveloperAccess
3. AmazonS3FullAccess

- Click Next.
- Name the role codeBuildServiceRole and create it.
- Add Inline Policy: 
- Find the codeBuildServiceRole, click Add permissions -> Create inline policy. Use the JSON editor and paste the following. Remember to replace the Resource ARN with your ECS Service ARN.

JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:UpdateService",
                "ecs:DescribeServices"
            ],
            "Resource": "<ENTER_YOUR_ECS_SERVICE_ARN>"
        }
    ]
}
- Name the policy ECSAccessPolicy and create it.

### Step 2: Create S3 Bucket for Artifacts
- Go to the S3 console -> Create bucket.
- Give it a globally unique name (e.g., 2048-pipeline-artifacts-yourname).
- Leave all other settings as default and create the bucket.

### Step 3: Create CodeBuild Project
- Go to the CodeBuild console -> Create build project.
- Project name: 2048-game-build.
- Source provider: GitHub. Connect to your GitHub account and choose the repository you created.
- Environment: Use the default managed image (aws/codebuild/standard:5.0).
- Service role: Choose Existing service role and select codeBuildServiceRole.
- Buildspec: Keep Use a buildspec file selected.

- Artifacts:
- Type: Amazon S3.
- Bucket name: Select the S3 bucket you created.
- Click Create build project.

### Step 4: Create the CodePipeline
- Go to the CodePipeline console -> Create pipeline.
- Pipeline name: 2048-game-pipeline.
- Service role: Let AWS create a new service role.
- Source stage:
- Provider: GitHub (Version 2).
- Create a new connection to your GitHub account. Select your repository and the main branch.

- Build stage:
- Provider: AWS CodeBuild.
- Project name: Select 2048-game-build.

- Deploy stage:
- Provider: Amazon ECS.
- Cluster name: Select 2048-game-cluster.
- Service name: Select 2048-service.

- Image definitions file: imagedefinitions.json.
- Review and Create pipeline.

## 6. Test the Pipeline
- In your local code, open index.html and change the h1 title to "2048 by Your Name".
- Commit and push the change to GitHub.

Bash

- git add .
- git commit -m "Test pipeline by changing title"
- git push origin main
- Go to the CodePipeline console and watch the pipeline automatically execute through the Source, Build, and Deploy stages.

- Once complete, refresh the browser tab with your ECS task's Public IP. You should see the updated title!

## 7. Project Clean-Up
* To avoid ongoing charges, delete the AWS resources in the following order:

* CodePipeline: Delete the 2048-game-pipeline.

* CodeBuild Project: Delete the 2048-game-build project.

* ECS Service & Cluster:

* First, update the 2048-service and set the number of tasks to 0.

* Once the task is stopped, delete the service.

* Finally, delete the 2048-game-cluster.

* ECR Repository: Delete the 2048-game-repo repository.

* S3 Bucket: Empty and then delete the artifacts bucket.

* IAM Roles: Delete the codeBuildServiceRole and the role created for CodePipeline (e.g., AWSCodePipelineServiceRole-us-east-1-2048-game-pipeline).
