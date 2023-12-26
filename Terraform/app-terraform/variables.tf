variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "service_name" {
  description = "Name of the service"
  type        = string
  default     = "tf-crud-app"
}

variable "env" {
  description = "Name of the service"
  type        = string
  default     = "task"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.2.0.0/16"
}

variable "vpc_cidr_pub" {
  description = "CIDR block for public subnets"
  type        = list(string)
  default     = ["10.2.1.0/24", "10.2.2.0/24"]
}

variable "vpc_cidr_priv" {
  description = "CIDR block for private subnets"
  type        = list(string)
  default     = ["10.2.11.0/24", "10.2.22.0/24"]
}

variable "access_rules" {
  type = list(object({
    port        = number
    proto       = string
    cidr_blocks = list(string)
  }))
  default = [
    {
      port        = 80
      proto       = "tcp"
      cidr_blocks = ["0.0.0.0/0", "109.251.117.23/32"]
    },
    {
      port        = 443
      proto       = "tcp"
      cidr_blocks = ["0.0.0.0/0", "109.251.117.23/32"]
    }
  ]
}

variable "instance_type" {
  description = "instance type"
  type        = string
  default     = "t2.micro"
}
