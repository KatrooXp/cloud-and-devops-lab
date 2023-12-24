## Terraform task

### Task architecture

![Alt text](<pics/Screenshot from 2023-10-25 13-22-10.png>)

### AWS resources used in this task

- Terraform tfstate file resourses: S3 bucket + DynamoDB table (created preliminary with Cloudformation)
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
- Route 53: hosted zone (created preliminary, in aws task)
- Certificate manager: public SSL certificate (created preliminary, in aws task)

### Create tfstate resources

- yaml file for Cloudformation: tfstate.backend.yaml

![Alt text](<pics/Screenshot from 2023-12-15 11-59-01.png>)

- resources deployed

![Alt text](<pics/Screenshot from 2023-12-15 12-01-08.png>)

- configure backend

![Alt text](<pics/Screenshot from 2023-12-15 12-17-43.png>)

### Terraform directory (app-terraform) structure

[app-terraform](app-terraform) /

->

[providers.tf](app-terraform/providers.tf)

[main.tf](app-terraform/main.tf)

[variables.tf](app-terraform/variables.tf)

[php-mysql-crud](app-terraform/php-mysql-crud)

[modules](app-terraform/modules) /

->

[modules/vpc](app-terraform/modules/vpc) 

    [vpc, subnets, igw, vpce-s3, route tables]

[modules/vpc/main.tf](app-terraform/modules/vpc/main.tf)

[modules/vpc/variables.tf](app-terraform/modules/vpc/variables.tf)

[modules/vpc/outputs.tf](app-terraform/modules/vpc/outputs.tf)

->

[modules/app](app-terraform/modules/app)  

    [app files (db.php) configuration, security groups, iam resources, s3 bucket create and upload, rds db resources, load balancer and listeners, autoscaling group and launch template, A-record in route53 hosted zone]

[modules/app/main.tf](app-terraform/modules/app/main.tf)

[modules/app/variables.tf](app-terraform/modules/app/variables.tf)

[modules/app/db.tpl](app-terraform/modules/app/db.tpl)

[modules/app/user-data.tpl](app-terraform/modules/app/user-data.tpl)

### main.tf

![Alt text](<pics/Screenshot from 2023-12-20 14-37-17.png>)

### Result

![Alt text](<pics/Screenshot from 2023-12-20 14-34-06.png>)






















