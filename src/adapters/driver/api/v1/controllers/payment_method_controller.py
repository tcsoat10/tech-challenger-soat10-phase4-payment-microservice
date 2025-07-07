
from typing import Optional

from src.application.usecases.payment_method_usecase.delete_payment_method_usecase import DeletePaymentMethodUseCase
from src.application.usecases.payment_method_usecase.update_payment_method_usecase import UpdatePaymentMethodUseCase
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.application.usecases.payment_method_usecase.get_all_payment_methods_usecase import GetAllPaymentMethodsUseCase
from src.application.usecases.payment_method_usecase.get_payment_method_by_id_usecase import GetPaymentMethodByIdUseCase
from src.application.usecases.payment_method_usecase.get_payment_method_by_name_usecase import GetPaymentMethodByNameUseCase
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.payment_method_usecase.create_payment_method_usecase import CreatePaymentMethodUseCase
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class PaymentMethodController:
    
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway: IPaymentMethodRepository = payment_method_gateway

    def create_payment_method(self, dto: CreatePaymentMethodDTO) -> PaymentMethodDTO:
        create_payment_method_use_case = CreatePaymentMethodUseCase.build(self.payment_method_gateway)
        payment_method = create_payment_method_use_case.execute(dto)
        return DTOPresenter.transform(payment_method, PaymentMethodDTO)
    
    def get_payment_method_by_name(self, name: str) -> PaymentMethodDTO:
        get_payment_method_by_name_use_case = GetPaymentMethodByNameUseCase.build(self.payment_method_gateway)
        payment_method = get_payment_method_by_name_use_case.execute(name)
        return DTOPresenter.transform(payment_method, PaymentMethodDTO)

    def get_payment_method_by_id(self, payment_method_id: str) -> PaymentMethodDTO:
        get_payment_method_by_id_use_case = GetPaymentMethodByIdUseCase.build(self.payment_method_gateway)
        payment_method = get_payment_method_by_id_use_case.execute(payment_method_id)
        return DTOPresenter.transform(payment_method, PaymentMethodDTO)

    def get_all_payment_methods(self, include_deleted: Optional[bool] = False) -> list[PaymentMethodDTO]:
        get_all_payment_methods_use_case = GetAllPaymentMethodsUseCase.build(self.payment_method_gateway)
        payment_methods = get_all_payment_methods_use_case.execute(include_deleted=include_deleted)
        return DTOPresenter.transform_list(payment_methods, PaymentMethodDTO)

    def update_payment_method(self, payment_method_id: int, dto: UpdatePaymentMethodDTO) -> PaymentMethodDTO:
        update_payment_method_use_case = UpdatePaymentMethodUseCase.build(self.payment_method_gateway)
        payment_method = update_payment_method_use_case.execute(payment_method_id, dto)
        return DTOPresenter.transform(payment_method, PaymentMethodDTO)

    def delete_payment_method(self, payment_method_id: int) -> None:
        delete_payment_method_use_case = DeletePaymentMethodUseCase.build(self.payment_method_gateway)
        delete_payment_method_use_case.execute(payment_method_id)
