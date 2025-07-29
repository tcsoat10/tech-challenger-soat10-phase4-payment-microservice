data "kubernetes_secret" "mongodb" {
  metadata {
    name      = "mongodb"
    namespace = "default"
  }
}

output "mongo_port" {
  value = 27017
}

output "mongo_uri" {
  value = "mongodb://${var.mongo_user}:${var.mongo_password}@mongodb:27017/${var.db_name}?authSource=${var.db_name}"
}

output "mongo_db" {
  value = var.db_name
}

output "mongo_user" {
  value = var.mongo_user
}

output "mongo_password" {
  value = var.mongo_password
  sensitive = true
}