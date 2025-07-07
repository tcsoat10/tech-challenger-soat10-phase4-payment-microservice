# Obtém a conexão com o banco de dados MongoDB config/database.py e executa a migração para popular os status de pagamento.

from config.database import connect_db
from src.constants.payment_status import PaymentStatusEnum
from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel

revision: str = '002'
down_revision: str = '001'
branch_labels: str | None = None
depends_on: str | None = None

payment_statuses = [*PaymentStatusEnum.values_and_descriptions()]

def upgrade() -> None:
    """
    Popula a coleção de status de pagamento com os status padrão.
    """
    # Ensure database connection
    connect_db()
    
    # Insere os status de pagamento no banco de dados usando MongoEngine
    for status in payment_statuses:
        existing_status = PaymentStatusModel.objects(name=status['name']).first()
        if not existing_status:
            payment_status = PaymentStatusModel(
                name=status['name'],
                description=status['description']
            )
            payment_status.save()
            print(f"Payment status '{status['name']}' inserted successfully.")
        else:
            print(f"Payment status '{status['name']}' already exists, skipping insertion.")

def downgrade() -> None:
    """
    Remove os status de pagamento inseridos na migração de upgrade.
    """
    # Ensure database connection
    connect_db()
    
    # Remove os status de pagamento padrão usando MongoEngine
    for status in payment_statuses:
        deleted_count = PaymentStatusModel.objects(name=status['name']).delete()
        if deleted_count > 0:
            print(f"Payment status '{status['name']}' removed successfully.")
        else:
            print(f"Payment status '{status['name']}' not found, skipping removal.")
