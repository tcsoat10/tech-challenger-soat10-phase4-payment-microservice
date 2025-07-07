
from typing import List

from src.application.usecases.payment_status_usecase.delete_payment_status_usecase import DeletePaymentStatusUseCase
from src.application.usecases.payment_status_usecase.update_payment_status_usecase import UpdatePaymentStatusUseCase
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.application.usecases.payment_status_usecase.get_all_payment_status_usecase import GetAllPaymentStatusUsecase
from src.application.usecases.payment_status_usecase.get_payment_status_by_id_usecase import GetPaymentStatusByIdUseCase
from src.application.usecases.payment_status_usecase.get_payment_status_by_name_usecase import GetPaymentStatusByNameUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.payment_status_usecase.create_payment_status_usecase import CreatePaymentStatusUseCase
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class PaymentStatusController:
    
    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway: IPaymentStatusRepository = payment_status_gateway

    def create_payment_status(self, dto: CreatePaymentStatusDTO) -> PaymentStatusDTO:
        create_payment_status_use_case = CreatePaymentStatusUseCase.build(self.payment_status_gateway)
        payment_status = create_payment_status_use_case.execute(dto)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)
    
    def get_payment_status_by_name(self, name: str) -> PaymentStatusDTO:
        get_payment_status_by_name_use_case = GetPaymentStatusByNameUseCase.build(self.payment_status_gateway)
        payment_status = get_payment_status_by_name_use_case.execute(name)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)
    
    def get_payment_status_by_id(self, payment_status_id: str) -> PaymentStatusDTO:
        get_payment_status_by_id_use_case = GetPaymentStatusByIdUseCase.build(self.payment_status_gateway)
        payment_status = get_payment_status_by_id_use_case.execute(payment_status_id)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)

    def get_all_payment_status(self, include_deleted: bool = False) -> List[PaymentStatusDTO]:
        get_all_payment_status_use_case = GetAllPaymentStatusUsecase.build(self.payment_status_gateway)
        payment_statuses = get_all_payment_status_use_case.execute(include_deleted)
        return DTOPresenter.transform_list(payment_statuses, PaymentStatusDTO)

    def update_payment_status(self, payment_status_id: int, dto: UpdatePaymentStatusDTO) -> PaymentStatusDTO:
        update_payment_status_use_case = UpdatePaymentStatusUseCase.build(self.payment_status_gateway)
        payment_status = update_payment_status_use_case.execute(payment_status_id, dto)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)

    def delete_payment_status(self, payment_status_id: int) -> None:
        delete_payment_status_use_case = DeletePaymentStatusUseCase.build(self.payment_status_gateway)
        delete_payment_status_use_case.execute(payment_status_id)
