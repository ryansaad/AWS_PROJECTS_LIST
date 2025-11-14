# Step-by-Step Project Instructions

Follow this guide to manually build and deploy a 3-Tier WordPress Architecture on AWS.

---

## 1. Networking Part 1: VPC, Subnets, and Routing

### Step 1.1: Create the VPC
1.  Navigate to the **VPC Dashboard** in the AWS Console.
2.  Click **Create VPC**. Select **VPC only**.
3.  **Name Tag**: `MyVPC`
4.  **IPv4 CIDR block**: `10.0.0.0/16`
5.  Click **Create VPC**.
6.  Select the new VPC, click **Actions** -> **Edit VPC settings**, and check **Enable DNS hostnames**.

### Step 1.2: Create and Attach Internet Gateway (IGW)
1.  In the VPC Dashboard, go to **Internet Gateways** -> **Create internet gateway**.
2.  **Name tag**: `MyIGW`. Click **Create**.
3.  Select the new IGW, click **Actions** -> **Attach to VPC**, and select `MyVPC`.

### Step 1.3: Create Subnets
1.  Go to **Subnets** -> **Create subnet**. Select `MyVPC`.
2.  Create the following **6 subnets**:
    * `PublicSubnet1`: AZ `us-east-1a`, CIDR `10.0.0.0/24`
    * `PublicSubnet2`: AZ `us-east-1b`, CIDR `10.0.1.0/24`
    * `PrivateAppSubnet1`: AZ `us-east-1a`, CIDR `10.0.2.0/24`
    * `PrivateAppSubnet2`: AZ `us-east-1b`, CIDR `10.0.3.0/24`
    * `PrivateDBSubnet1`: AZ `us-east-1a`, CIDR `10.0.4.0/24`
    * `PrivateDBSubnet2`: AZ `us-east-1b`, CIDR `10.0.5.0/24`
3.  Click **Create subnets**.

### Step 1.4: Create Route Tables
1.  Go to **Route Tables** -> **Create route table**.
2.  **Public Route Table**:
    * Name: `PublicRouteTable`, VPC: `MyVPC`.
    * Add a route: Destination `0.0.0.0/0`, Target `MyIGW`.
    * Associate `PublicSubnet1` and `PublicSubnet2`.
3.  **Private Route Table (AZ1)**:
    * Name: `PrivateRouteTableAZ1`, VPC: `MyVPC`.
    * Associate `PrivateAppSubnet1` and `PrivateDBSubnet1`.
4.  **Private Route Table (AZ2)**:
    * Name: `PrivateRouteTableAZ2`, VPC: `MyVPC`.
    * Associate `PrivateAppSubnet2` and `PrivateDBSubnet2`.

---

## 2. Networking Part 2: NAT Gateways & Security Groups

### Step 2.1: Create NAT Gateways
1.  In the VPC Dashboard, go to **Elastic IPs** and **Allocate** two new Elastic IP addresses.
2.  Navigate to **NAT Gateways** -> **Create NAT gateway**.
3.  **NAT Gateway 1**: Name `NATGateway1`, Subnet `PublicSubnet1`, assign the first Elastic IP.
4.  **NAT Gateway 2**: Name `NATGateway2`, Subnet `PublicSubnet2`, assign the second Elastic IP.
5.  Update the private route tables:
    * In `PrivateRouteTableAZ1`, add a route: Destination `0.0.0.0/0`, Target `NATGateway1`.
    * In `PrivateRouteTableAZ2`, add a route: Destination `0.0.0.0/0`, Target `NATGateway2`.

### Step 2.2: Create Security Groups
1.  Navigate to **Security Groups** -> **Create security group**.
2.  Create the following security groups within `MyVPC`:
    * **ALBSecurityGroup**: Inbound HTTP (80) & HTTPS (443) from `0.0.0.0/0`.
    * **WebServerSecurityGroup**: Inbound HTTP (80) & HTTPS (443) from `ALBSecurityGroup`.
    * **DatabaseSecurityGroup**: Inbound MySQL/Aurora (3306) from `WebServerSecurityGroup`.
    * **EFSSecurityGroup**: Inbound NFS (2049) from `WebServerSecurityGroup` and a second self-referencing rule for NFS (2049) from `EFSSecurityGroup` itself.
    * **SSHSecurityGroup**: Inbound SSH (22) from **My IP**.

---

## 3. Database and Storage Setup

### Step 3.1: Create DB Subnet Group
1.  Navigate to the **RDS Dashboard**.
2.  Go to **Subnet groups** -> **Create DB subnet group**.
3.  **Name**: `MyDBSubnetGroup`, **VPC**: `MyVPC`.
4.  Add the two private DB subnets (`10.0.4.0/24` and `10.0.5.0/24`).

### Step 3.2: Create the RDS MySQL Database
1.  In the RDS Dashboard, click **Create database**.
2.  **Method**: Standard Create, **Engine**: MySQL, **Template**: Free Tier.
3.  **Settings**:
    * **DB instance identifier**: `MyMySQLDatabase`
    * **Master username/password**: Set your credentials.
4.  **Connectivity**:
    * **VPC**: `MyVPC`, **Subnet group**: `MyDBSubnetGroup`.
    * **Public access**: No.
    * **VPC security group**: Choose `DatabaseSecurityGroup`.
5.  Click **Create database**.

### Step 3.3: Create Elastic File System (EFS)
1.  Navigate to the **EFS Dashboard** -> **Create file system**.
2.  **Name**: `MyEFS`, **VPC**: `MyVPC`.
3.  Click **Customize**.
4.  Under **Network access**, ensure mount targets are created in `PrivateAppSubnet1` and `PrivateAppSubnet2`.
5.  For each mount target, assign the `EFSSecurityGroup`.
6.  Click **Create**.

---

## 4. Compute and Application Setup

### Step 4.1: Launch a Temporary Public EC2 for Setup
1.  Go to the **EC2 Dashboard** -> **Launch instance**.
2.  **Name**: `WordPress-Setup-Instance`.
3.  **AMI**: Amazon Linux. **Instance Type**: `t2.micro`.
4.  **Key pair**: Create or select a `.ppk` key pair for PuTTY.
5.  **Network**: `MyVPC`, Subnet `PublicSubnet1`, enable Auto-assign Public IP.
6.  **Security Groups**: Select `WebServerSecurityGroup`, `ALBSecurityGroup`, and `SSHSecurityGroup`.
7.  Launch the instance.

### Step 4.2: Configure WordPress on the Setup Instance
1.  Connect to the instance via SSH (using its public IP).
2.  Run the following commands to install software and configure WordPress on the EFS mount:
    ```bash
    # Switch to root user and update
    sudo su
    yum update -y

    # Install Apache, PHP, and MySQL client
    yum install -y httpd php php-mysqlnd
    
    # Mount EFS (get the command from the EFS console 'Attach' button)
    mkdir -p /var/www/html
    # Example: mount -t nfs4 -o nfsvers=4.1,rsize=... <YOUR_EFS_DNS>:/ /var/www/html
    
    # Set permissions and start services
    systemctl enable httpd
    systemctl start httpd
    chown -R apache:apache /var/www/html

    # Download and configure WordPress
    cd /var/www/html
    wget [https://wordpress.org/latest.tar.gz](https://wordpress.org/latest.tar.gz)
    tar -xzf latest.tar.gz
    cp -r wordpress/* .
    rm -rf wordpress latest.tar.gz

    # Create and edit config file
    cp wp-config-sample.php wp-config.php
    nano wp-config.php 
    # --> Update DB_NAME, DB_USER, DB_PASSWORD, and DB_HOST (RDS Endpoint)
    ```
3.  Access the public IP of your setup instance in a browser and complete the WordPress installation.

### Step 4.3: Launch Private Application Servers
1.  Create an AMI from your configured `WordPress-Setup-Instance`.
2.  Launch two new `t2.micro` instances from this AMI:
    * **ApplicationServer1**: Launch in `PrivateAppSubnet1`.
    * **ApplicationServer2**: Launch in `PrivateAppSubnet2`.
    * For both, assign the `WebServerSecurityGroup` and `SSHSecurityGroup`.

### Step 4.4: Create and Configure Application Load Balancer (ALB)
1.  Go to **Load Balancers** -> **Create Load Balancer**.
2.  **Type**: Application Load Balancer.
3.  **Name**: `MyALB`, **Scheme**: `Internet-facing`.
4.  **Network**: `MyVPC`, map it to `PublicSubnet1` and `PublicSubnet2`.
5.  **Security Groups**: Select `ALBSecurityGroup`.
6.  **Listeners**: For the HTTP:80 listener, create a new **Target Group**.
    * **Target type**: Instances.
    * **Name**: `MyAppServers`, **VPC**: `MyVPC`.
    * Register `ApplicationServer1` and `ApplicationServer2` as targets.
7.  Create the load balancer.

### Step 4.5: Finalize
1.  Access your WordPress site using the ALB's DNS name.
2.  Log in to `/wp-admin` and update the **WordPress Address** and **Site Address** in Settings -> General to the ALB's DNS name.
3.  Once confirmed working, **terminate** the temporary `WordPress-Setup-Instance`.

---

## 5. Project Clean-Up

To avoid ongoing charges, delete resources in the following order:
1.  Application Load Balancer (`MyALB`).
2.  EC2 Instances (`ApplicationServer1`, `ApplicationServer2`).
3.  RDS Database (`MyMySQLDatabase`). Remember to handle final snapshots if needed.
4.  EFS File System (`MyEFS`).
5.  NAT Gateways (This also releases the Elastic IPs).
6.  Internet Gateway (`MyIGW`).
7.  VPC (This will also delete associated subnets, route tables, etc.).
8.  Security Groups and IAM Roles.
