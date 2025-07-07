# Obtém a conexão com o banco de dados MongoDB config/database.py e executa a migração para popular os métodos de pagamento.
# metodos de pagamento: qr_code

from config.database import connect_db
from src.constants.payment_method_enum import PaymentMethodEnum
from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel

revision: str = '001'
down_revision: str = None
branch_labels: str | None = None
depends_on: str | None = None

payment_methods = [*PaymentMethodEnum.values_and_descriptions()]

def upgrade() -> None:
    """
    Popula a coleção de métodos de pagamento com os métodos padrão.
    """
    # Ensure database connection
    connect_db()
    
    # Insere os métodos de pagamento no banco de dados usando MongoEngine
    for method in payment_methods:
        existing_method = PaymentMethodModel.objects(name=method['name']).first()
        if not existing_method:
            payment_method = PaymentMethodModel(
                name=method['name'],
                description=method['description']
            )
            payment_method.save()
            print(f"Payment method '{method['name']}' inserted successfully.")
        else:
            print(f"Payment method '{method['name']}' already exists, skipping insertion.")

def downgrade() -> None:
    """
    Remove os métodos de pagamento inseridos na migração de upgrade.
    """
    # Ensure database connection
    connect_db()
    
    # Remove os métodos de pagamento padrão usando MongoEngine
    for method in payment_methods:
        deleted_count = PaymentMethodModel.objects(name=method['name']).delete()
        if deleted_count > 0:
            print(f"Payment method '{method['name']}' removed successfully.")
        else:
            print(f"Payment method '{method['name']}' not found, skipping removal.")
