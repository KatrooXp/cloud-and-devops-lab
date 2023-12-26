# db.php file and userdata configuration

data "template_file" "db-php" {
  template = "${file("${path.module}/db.tpl")}"
  vars = {
    db_cluster = "${aws_rds_cluster.db_mysql.endpoint}"
    db_password = "${var.service_name}-${var.env}-db-password"
  }
}

resource "local_file" "db-php" {
  content  = "${data.template_file.db-php.rendered}"
  filename = "php-mysql-crud/db.php"
}

data "template_file" "user-data" {
  template = "${file("${path.module}/user-data.tpl")}"
  vars = {
    db_cluster = "${aws_rds_cluster.db_mysql.endpoint}"
    db_password = "${var.service_name}-${var.env}-db-password"
  }
}

# Security groups:
  # epam-lab-cloud-ASG (allows inbound traffic from VPC to port 80 - HTTP)
  # epam-lab-cloud-RDS (allows inbound traffic from ASG security group to port 3306 - MySQL/Aurora)
  # epam-lab-cloud-LB (allows inbound traffic from selected IP addresses to ports 443 - HTTPS and 80 - HTTP)

resource "aws_security_group" "asg-sg" {
  name        = "${var.service_name}-${var.env}-asg-sg"
  description = "ASG SG: allows inbound traffic from VPC to port 80 - HTTP"
  vpc_id      = var.vpc_id

  ingress {
    description = "allow inbound traffic from VPC, port 80"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.service_name}-${var.env}-asg-sg"
  }
}

resource "aws_security_group" "rds-sg" {
  name        = "${var.service_name}-${var.env}-rds-sg"
  description = "RDS SG: allows inbound traffic from ASG security group to port 3306 - MySQL/Aurora"
  vpc_id      = var.vpc_id

  ingress {
    description     = "allow inbound traffic from asg-sg, port 3306"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = ["${aws_security_group.asg-sg.id}"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.service_name}-${var.env}-rds-sg"
  }
}

resource "aws_security_group" "lb-sg" {
  name        = "${var.service_name}-${var.env}-lb-sg"
  description = "ASG SG: allows inbound traffic from VPC to port 80 - HTTP"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.access_rules
    content {
      from_port   = ingress.value["port"]
      to_port     = ingress.value["port"]
      protocol    = ingress.value["proto"]
      cidr_blocks = ingress.value["cidr_blocks"]
    }
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.service_name}-${var.env}-lb-sg"
  }
}

# S3: bucket with public access blocked

resource "aws_s3_bucket" "s3-bucket" {
  bucket = "${var.service_name}-${var.env}-s3-bucket"

  tags = {
    Name = "${var.service_name}-${var.env}-s3-bucket"
  }
}

resource "aws_s3_bucket_public_access_block" "s3-bucket" {
  bucket = aws_s3_bucket.s3-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "s3-upload" {
  bucket = aws_s3_bucket.s3-bucket.id
  
  for_each = fileset("php-mysql-crud/", "**/*")

  key = "php-mysql-crud/${each.value}"
  source = "php-mysql-crud/${each.value}"
}

# IAM: role for EC2, policy with permission to download from S3 bucket and instance profile with this role

resource "aws_iam_role" "s3-download" {
  name = "${var.service_name}-${var.env}-s3-download-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name = "${var.service_name}-${var.env}-s3-download-role"
  }
}

resource "aws_iam_role_policy" "s3-download" {
  name = "${var.service_name}-${var.env}-s3-download-policy"
  role = aws_iam_role.s3-download.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListBucket",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::*"
      },
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::*/*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "s3-download" {
  name = "${var.service_name}-${var.env}-s3-download-instance-profile"
  role = aws_iam_role.s3-download.name
}

# RDS: Aurora (MySQL) database 5.7.mysql_aurora.2.11.3 with autopause

resource "aws_db_subnet_group" "db_mysql" {
  name       = "${var.service_name}-${var.env}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.service_name}-${var.env}-db-subnet-group"
  }
}

resource "aws_rds_cluster" "db_mysql" {
  cluster_identifier = "${var.service_name}-${var.env}-db-cluster"
  engine             = "aurora-mysql"
  engine_version     = "5.7.mysql_aurora.2.11.4"
  engine_mode        = "serverless"
  database_name      = "php_mysql_crud"
  master_username    = "admin"
  master_password    = "${var.service_name}-${var.env}-db-password"
  scaling_configuration {
    auto_pause               = true
    max_capacity             = 1
    min_capacity             = 1
    seconds_until_auto_pause = 1200
  }
  db_subnet_group_name   = aws_db_subnet_group.db_mysql.id
  vpc_security_group_ids = [aws_security_group.rds-sg.id]

  skip_final_snapshot = true  #to let terraform destroy rds cluster and eligible resources with terraform destroy command
  apply_immediately = true

  tags = {
    Name = "${var.service_name}-${var.env}-db-cluster"
  }
  
  lifecycle {
  ignore_changes = [
    engine_version
    ]
  }

}

# EC2:
  # Target group

resource "aws_lb_target_group" "tg" {
  name     = "${var.service_name}-${var.env}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  health_check {
    enabled = true
    path = "/health.html"
  }

  tags = {
    Name = "${var.service_name}-${var.env}-tg"
  }
}

  # Application Load balancer with 2 listeners

resource "aws_lb" "lb" {
  name               = "${var.service_name}-${var.env}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb-sg.id]
  subnets            = var.public_subnet_ids

  tags = {
    Name = "${var.service_name}-${var.env}-lb"
  }
}

data "aws_acm_certificate" "certificate" {
  domain   = "katroo.pp.ua"
  statuses = ["ISSUED"]
}

resource "aws_lb_listener" "https-forward" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = data.aws_acm_certificate.certificate.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

resource "aws_lb_listener" "http-redirect" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

  # Launch template

resource "aws_launch_template" "lt" {
  name          = "${var.service_name}-${var.env}-lt"
  image_id      = "ami-01eccbf80522b562b"
  instance_type = var.instance_type
  iam_instance_profile {
    arn = aws_iam_instance_profile.s3-download.arn
  }
  vpc_security_group_ids = [aws_security_group.asg-sg.id]
  
  user_data = base64encode(data.template_file.user-data.rendered)

  tags = {
    Name = "${var.service_name}-${var.env}-lt"
  }
}

  # Auto scalig group 

resource "aws_autoscaling_group" "asg" {
  name = "${var.service_name}-${var.env}-asg"
  target_group_arns = ["${aws_lb_target_group.tg.arn}"]
  vpc_zone_identifier = var.private_subnet_ids
  desired_capacity   = 1    
  min_size           = 1    
  max_size           = 3    
  health_check_type = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.lt.id
    version = "$Latest"
  }

}

resource "aws_autoscaling_policy" "asg" {
  name = "${var.service_name}-${var.env}-autoscaling-policy"
  autoscaling_group_name = aws_autoscaling_group.asg.id
  policy_type = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label = "${aws_lb.lb.arn_suffix}/${aws_lb_target_group.tg.arn_suffix}"
    }
    target_value = 10
  }

}

# Create A-record in hosted zone

data "aws_route53_zone" "zone" {
  name         = "katroo.pp.ua"
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = data.aws_route53_zone.zone.name
  type    = "A"

  alias {
    name                   = aws_lb.lb.dns_name
    zone_id                = aws_lb.lb.zone_id
    evaluate_target_health = true
  }
}
