variable "region" {
  description = "AWS region"
  type        = string
}

variable "service_name" {
  description = "Name of the service"
  type        = string
}

variable "env" {
  description = "Name of the service"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "vpc_cidr_pub" {
  description = "CIDR block for public subnets"
  type        = list(string)
}

variable "vpc_cidr_priv" {
  description = "CIDR block for private subnets"
  type        = list(string)
}
