output "payment_app_lb_endpoint" {
  description = "Endpoint do Load Balancer do payment-app"
  value       = kubernetes_service.payment_app_lb.status[0].load_balancer[0].ingress[0].hostname
}