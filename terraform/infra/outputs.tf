output "eks_cluster_name" {
  value = aws_eks_cluster.cluster.name
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.cluster.endpoint
}

output "eks_cluster_ca" {
  value = aws_eks_cluster.cluster.certificate_authority[0].data
}

data "aws_instances" "eks_nodes" {
  filter {
    name   = "tag:eks:nodegroup-name"
    values = [aws_eks_node_group.eks-node.node_group_name]
  }
}

output "eks_nodes_public_ips" {
  value       = data.aws_instances.eks_nodes.public_ips
  description = "Lista de IPs públicos dos nodes do EKS"
}