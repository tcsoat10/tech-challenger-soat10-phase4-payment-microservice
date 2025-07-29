variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "mongo_password" {
  description = "Database user password"
  type        = string
}

variable "mongo_db" {
  default = "payment_service"
}

variable "mongo_user" {
  description = "Database username"
  type        = string
}

variable "payment_service_api_key" {
  description = "API key for payment microservice"
  type        = string
}

variable "mongo_host" {
  type        = string
  default = ""
}

variable "mongo_port" {
  type        = string
  default = "27017"
}