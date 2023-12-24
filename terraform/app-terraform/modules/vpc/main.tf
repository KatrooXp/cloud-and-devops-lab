data "aws_availability_zones" "available_zones" {}

# VPC

resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.service_name}-${var.env}-vpc"
  }
}

# Subnets (4): 2 public and 2 private subnets located in 2 availiability zones (1 pulic and 1 private in each AZ)

resource "aws_subnet" "public_subnets" {
  count = length(var.vpc_cidr_pub)

  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.vpc_cidr_pub[count.index]
  availability_zone = data.aws_availability_zones.available_zones.names[count.index]

  tags = {
    Name = "${var.service_name}-${var.env}-subnet-pub-${count.index + 1}"
  }
}

resource "aws_subnet" "private_subnets" {
  count = length(var.vpc_cidr_priv)

  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.vpc_cidr_priv[count.index]
  availability_zone = data.aws_availability_zones.available_zones.names[count.index]

  tags = {
    Name = "${var.service_name}-${var.env}-subnet-priv-${count.index + 1}"
  }

}

# Internet gateway, attached to public vpc

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.service_name}-${var.env}-igv"
  }
}

# VPC endpoint: com.amazonaws.us-east-1.s3

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.vpc.id
  service_name = "com.amazonaws.${var.region}.s3"

  tags = {
    Name = "${var.service_name}-${var.env}-vpce-s3"
  }
}

# Route tables (3): 1 for public subnets and 2 for private subnets (1 for each)

resource "aws_route_table" "rtb_pub" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.service_name}-${var.env}-rtb-pub"
  }
}

resource "aws_route_table_association" "rtb_pub" {
  count = length(var.vpc_cidr_pub)

  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.rtb_pub.id
}

resource "aws_route_table" "rtb_priv" {
  vpc_id = aws_vpc.vpc.id
  count  = length(var.vpc_cidr_priv)

  tags = {
    Name = "${var.service_name}-${var.env}-rtb-priv-${count.index + 1}-az-${data.aws_availability_zones.available_zones.names[count.index]}"
  }
}

resource "aws_route_table_association" "rtb_priv" {
  count = length(var.vpc_cidr_priv)

  subnet_id      = aws_subnet.private_subnets[count.index].id
  route_table_id = aws_route_table.rtb_priv[count.index].id
}

resource "aws_vpc_endpoint_route_table_association" "rtb_priv" {
  count = length(var.vpc_cidr_priv)

  route_table_id  = aws_route_table.rtb_priv[count.index].id
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}