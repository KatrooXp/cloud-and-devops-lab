## AWS task

*Below, this Readme shows this task configured via console, with screenshots and explanations*

### Task architecture

![Alt text](<pics/Screenshot from 2023-10-25 13-22-10.png>)

### Resources used in this task
- VPC: epam-lab-cloud-vpc
    - Subnets (4): 2 public and 2 private subnets located in 2 availiability zones (1 pulic and 1 private in each AZ)
    - Route tables (3): 1 for public subnets and 2 for private subnets (1 for each)
    - Internet gateway, attached to public vpc
    - VPC endpoint: com.amazonaws.us-east-1.s3
- Security groups: 
    - epam-lab-cloud-ASG (allows inbound traffic from VPC to port 80 - HTTP)
    - epam-lab-cloud-RDS (allows inbound traffic from epam-lab-cloud-ASG security group to port 3306 - MySQL/Aurora)
    - epam-lab-cloud-LB (allows inbound traffic from selected IP addresses to ports 443 - HTTPS and 80 - HTTP)
- S3: bucket with public access blocked
- IAM: role for EC2 with permission to download from S3 bucket
- RDS: Aurora (MySQL) database
- EC2:
    - Target group
    - Application Load balancer with 2 listeners
    - Launch template
    - Auto scalig group
- Route 53: hosted zone
- Certificate manager: public SSL certificate

### Create a VPC

![Alt text](<pics/Screenshot from 2023-10-25 17-06-16.png>)
![Alt text](<pics/Screenshot from 2023-10-25 17-14-18.png>)

Route tables configuration:

- public route table has two routes: local (for connections in the VPC) and to igw (for Internet connections)

![Alt text](<pics/Screenshot from 2023-10-25 17-30-12.png>)

- private route tables are identic and each has two routes: local and to S3 VPC endpoints (to connect with S3 service). 

    If Internet connection for private subnet is needed the route to NAT gateway is to be added to the corresponding route table (destination: 0.0.0.0/0, target: nat-gateway-id)

![Alt text](<pics/Screenshot from 2023-10-25 17-35-12.png>)

### Create S3 bucket and IAM role for EC2

- S3 bucket

![Alt text](<pics/Screenshot from 2023-10-26 17-52-02.png>)

- IAM role for EC2 to download from S3 bucket

![Alt text](<pics/Screenshot from 2023-10-26 17-54-02.png>)
![Alt text](<pics/Screenshot from 2023-10-26 17-54-35.png>)

- policy with permissions

![Alt text](<pics/Screenshot from 2023-10-26 17-56-12.png>)

- after the db is created, edit the connection details and sql script in the code and upload to S3 bucket

![Alt text](<pics/Screenshot from 2023-10-27 17-31-33.png>)

![Alt text](<pics/Screenshot from 2023-10-31 11-13-46.png>)

### Create RDS Aurora (MySQL) database

- choose Aurora (MySQL Compatible), version 5.7.2.11.3 - compatible with serverless v1

![Alt text](<pics/Screenshot from 2023-10-26 18-47-00.png>)

- configure db cluster name and credentials

![Alt text](<pics/Screenshot from 2023-10-26 18-48-14.png>)

- choose db instance class - serverless v1 (because it has option to pause db after inactivity), choose minimum and maximum capacity

![Alt text](<pics/Screenshot from 2023-10-26 18-52-01.png>)

- choose VPC and create SG

![Alt text](<pics/Screenshot from 2023-10-26 19-01-06.png>)

- set initial db name

![Alt text](<pics/Screenshot from 2023-10-26 19-02-58.png>)

- SG rules (allow inbound traffic only from machines of ASG security group):

![Alt text](<pics/Screenshot from 2023-10-30 13-52-34.png>)

### Create Target Group

![Alt text](<pics/Screenshot from 2023-10-28 17-35-26.png>)
![Alt text](<pics/Screenshot from 2023-10-28 17-36-10.png>)

- *change path to healthcheck to /health.html, add file health.html to S3 bucket - to not trigger db on each healthcheck* 

![Alt text](<pics/Screenshot from 2023-10-30 13-32-35.png>)

### Create Application Load Balancer

![Alt text](<pics/Screenshot from 2023-10-28 17-42-00.png>)

- configure listeners: 443 to target group

![Alt text](<pics/Screenshot from 2023-10-28 19-19-51.png>)
![Alt text](<pics/Screenshot from 2023-10-28 19-20-47.png>)

- configure listeners: 80 to 443

![Alt text](<pics/Screenshot from 2023-10-28 19-22-47.png>)

- Load balancer Security Group (allows traffic only from my ip)

![Alt text](<pics/Screenshot from 2023-10-30 13-57-54.png>)

### Create Auto Scaling Group

- Create launch template, choose SG, add IAM profile and userdata

![Alt text](<pics/Screenshot from 2023-10-27 17-42-47.png>)
![Alt text](<pics/Screenshot from 2023-10-27 18-01-56.png>)
![Alt text](<pics/Screenshot from 2023-10-27 18-02-37.png>)
![Alt text](<pics/Screenshot from 2023-10-27 19-31-21.png>)
![Alt text](<pics/Screenshot from 2023-10-31 11-26-32.png>)

- SG rules: 

![Alt text](<pics/Screenshot from 2023-10-28 17-33-19.png>)

- Create Auto Scaling group

![Alt text](<pics/Screenshot from 2023-10-28 17-13-11.png>)

- choose private subnets

![Alt text](<pics/Screenshot from 2023-10-28 17-17-31.png>)

- choose "attach to an existing LB", choose the load balancer target group

![Alt text](<pics/Screenshot from 2023-10-28 17-18-10.png>)

- turn on ELB health checks

![Alt text](<pics/Screenshot from 2023-10-28 17-19-14.png>)

- specify the capacity and scaling policies

![Alt text](<pics/Screenshot from 2023-10-28 17-20-30.png>)

## Create hosted zone Route53

![Alt text](<pics/Screenshot from 2023-10-28 19-14-22.png>)

## Get SSL certificate

- *before LB listeners configuration*

![Alt text](<pics/Screenshot from 2023-10-28 19-15-47.png>)

## Test the auto scaling

- generate multiple requests

![Alt text](<pics/Screenshot from 2023-10-28 20-17-11.png>)

- cloudwatch alarm

![Alt text](<pics/Screenshot from 2023-10-28 20-14-33.png>)

- autoscaling group launching new instances

![Alt text](<pics/Screenshot from 2023-10-28 20-14-18.png>)

- target group

![Alt text](<pics/Screenshot from 2023-10-28 20-16-55.png>)























