provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc-payment-app"
    key    = "payment-microservice/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

resource "kubernetes_deployment" "payment_app" {
  metadata {
    name      = "payment-app"
    namespace = "default"
    labels = {
      app = "payment-app"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "payment-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "payment-app"
        }
      }
      spec {
        container {
          name  = "payment-app"
          image = "086134737169.dkr.ecr.us-east-1.amazonaws.com/soattc-payment-app:latest"
          env{
            name = "MONGO_HOST"
            value = "mongodb"
          }
          env {
            name  = "MONGO_DB"
            value = data.terraform_remote_state.mongo.outputs.mongo_db
          }
          env {
            name  = "MONGO_USER"
            value = data.terraform_remote_state.mongo.outputs.mongo_user
          }
          env {
            name  = "MONGO_PASSWORD"
            value = data.terraform_remote_state.mongo.outputs.mongo_password
          }
          env {
            name  = "MONGO_PORT"
            value = var.mongo_port
          }
          env {
            name = "PAYMENT_SERVICE_API_KEY"
            value = var.payment_service_api_key
          }
          env {
            name  = "MONGO_URI"
            value = data.terraform_remote_state.mongo.outputs.mongo_uri
          }
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "payment_app_lb" {
  depends_on = [kubernetes_deployment.payment_app]
  metadata {
    name      = "payment-app-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "payment-app"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8001
    }
  }
}