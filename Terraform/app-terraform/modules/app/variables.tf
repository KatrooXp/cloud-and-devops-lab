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

variable "vpc_id" {
  description = "VPC id"
  type        = string
}

variable "access_rules" {
  type = list(object({
    port        = number
    proto       = string
    cidr_blocks = list(string)
  }))
}

variable "private_subnet_ids" {
  description = "private subnet id"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "public subnet id"
  type        = list(string)
}

variable "instance_type" {
  description = "instance type"
  type        = string
}

variable "ssl_policy" {
  description = "ssl policy"
  type        = string
  default     = "ELBSecurityPolicy-TLS13-1-0-2021-06"
}

# variable "ssl_sertificate" {
#   description = "ssl sertificate arn"
#   type        = string
#   default     = "arn:aws:acm:us-east-1:178851004264:certificate/3d89493e-8be5-40b4-b7eb-aa6ba63d5737"
# }