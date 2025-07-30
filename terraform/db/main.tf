terraform {
  backend "s3" {
    bucket = "soattc-payment-db"
    key    = "payment-db/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

provider "helm" {
  kubernetes = {
    host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
    cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

resource "helm_release" "mongodb" {
  name       = "mongodb"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "mongodb"
  version    = "16.5.33"

  set = [
    {
      name  = "auth.enabled"
      value = "true"
    },
    {
      name  = "architecture"
      value = "standalone"
    },
    {
      name  = "replicaCount"
      value = "1"
    },
    {
      name  = "persistence.enabled"
      value = "false"
    },
    {
      name  = "auth.username"
      value = var.mongo_user
    },
    {
      name  = "auth.password"
      value = var.mongo_password
    },
    {
      name  = "auth.database"
      value = var.db_name
    },
    {
      name  = "auth.rootPassword"
      value = var.mongo_root_password
    }
  ]
}