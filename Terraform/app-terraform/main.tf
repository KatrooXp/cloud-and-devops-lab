terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.48.0"
    }
  }

  backend "s3" {
    key            = "terraform.tfstate"
    bucket         = "tfstate-bucket-katroo"
    region         = "us-east-1"
    dynamodb_table = "tfstate-lock-ddb"
  }
  # terraform init -backend-config='key=<service_name>/<env>/terraform.tfstate'
}

module "vpc" {
  source        = "./modules/vpc"
  region        = var.region
  service_name  = var.service_name
  env           = var.env
  vpc_cidr      = var.vpc_cidr
  vpc_cidr_pub  = var.vpc_cidr_pub
  vpc_cidr_priv = var.vpc_cidr_priv
}

module "app" {
  source        = "./modules/app"
  service_name  = var.service_name
  env           = var.env
  vpc_id        = module.vpc.vpc_id
  vpc_cidr      = var.vpc_cidr
  access_rules  = var.access_rules
  private_subnet_ids = module.vpc.private_subnets
  public_subnet_ids = module.vpc.public_subnets
  instance_type = var.instance_type
}









