# Payment Microservice - SOAT10 - Pós Tech Arquitetura de Software - FIAP

# Tópicos
- [Tech Challenge - Grupo 30 SOAT10 - Pós Tech Arquitetura de Software - FIAP](#tech-challenge---grupo-30-soat10---pós-tech-arquitetura-de-software---fiap)
- [Tópicos](#tópicos)
- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Executando o Projeto](#executando-o-projeto)
- [Comunicação com os demais serviços](#comunicação-com-os-demais-serviços)
- [Secrets Necessários](#secrets-necessários)


# Descrição do Projeto

O projeto visa atender à demanda de uma lanchonete de bairro, que, devido ao seu sucesso, necessita implementar um sistema de autoatendimento. 

Esta aplicação é parte de um ecossistema distribuído em seis repositórios, executando inteiramente na AWS, com deploy via Terraform.
Distribuído em micro serviços, onde cada um exerce sua função, todos sendo analisados pelo SonarQube para garantir a qualidade do Software.

 [Topo](#tópicos)

# Tecnologias Utilizadas
- [Python 3.12](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [MongoDB](https://www.mongodb.com/)
- [Kubernetes](https://kubernetes.io/)
- [Terraform](https://developer.hashicorp.com/terraform)
- [AWS Relational Database Service (RDS)](https://aws.amazon.com/pt/rds/)
- [AWS Elastic Kubernetes Service (EKS)](https://aws.amazon.com/pt/eks/)
- [AWS Elastic Container Registry (ECR)](https://aws.amazon.com/pt/ecr/)

- [Github Actions](https://github.com/features/actions)

 [Topo](#tópicos)

# Executando o Projeto
Este projeto não é executado localmente. O deploy ocorre automaticamente na AWS via GitHub Actions, fazendo uso do Terraform.

Este projeto está estruturado em seis repositórios:
1 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-eks-infra);
2 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-sonarqube);
3 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-auth-microservice);
4 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-supply-microservice);
5 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-order-microservice);
6 - Infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase4-payment-microservice);

 [Topo](#tópicos)

# Comunicação com os demais serviços

- O deploy da infra Kubernetes é feito em um cluster EKS. Dentro deste cluster, o deploy da aplicação é feito em um pod, e tem seu acesso gerenciado por um Load Balancer.
- A aplicação enxerga o banco de dados disponível e realiza as migrações necessárias.

 [Topo](#tópicos)

# Secrets Necessários
- AWS_ACCESS_KEY_ID: Access Key ID da conta AWS
- AWS_ACCOUNT_ID: Account ID da conta AWS
- AWS_SECRET_ACCESS_KEY: Secret Access Key da conta AWS
- AWS_SESSION_TOKEN: token de sessão da conta da AWS, necessário para contas temporárias, como da AWS Academy
- AWS_EKS_CLUSTER_NAME: nome do cluster EKS onde a aplicação estará hospedada
- MERCADO_PAGO_ACCESS_TOKEN: token de acesso da API do Mercado Pago
- MERCADO_PAGO_POS_ID: ID do PoS do Mercado Pago
- MERCADO_PAGO_USER_ID: ID do usuário do Mercado Pago
- MYSQL_DATABASE: nome do banco de dados MySQL
- MYSQL_HOST: hostname do banco MySQL, neste caso, o endpoint do RDS
- MYSQL_PORT: porta do banco
- MYSQL_USER: usuário do banco
- MYSQL_PASSWORD: senha do usuário do banco
- WEBHOOK_URL: url do webhook que recebe as respostas da API do Mercado Pago para confirmação do pagamento
- SECRET_KEY: chave secreta do token JWT
- SONAR_HOST_URL: URL do serviço SonarQube
- SONAR_TOKEN: Token de acesso ao serviço SonarQube
- STOCK_MICROSERVICE_API_KEY: Chave da API do micro serviço de Estoque
- STOCK_MICROSERVICE_URL: URL para acessar o micro serviço de Estoque
- ORDER_MICROSERVICE_API_KEY: Chave da API do micro serviço de Pedido
- PAYMENT_NOTIFICATION_URL: URL para acessar o serviço de notificação
- PAYMENT_SERVICE_API_KEY: Chave da API do micro serviço de Pedido
- PAYMENT_SERVICE_URL: URL para acessar o micro serviço de Pagamento


 [Topo](#tópicos)

# Diagrama de Arquitetura
![Diagrama de arquitetura fase 4](https://github.com/user-attachments/assets/8d69433d-fdfd-4d5a-bf4b-fc9297409d9d)

[Topo](#tópicos)
