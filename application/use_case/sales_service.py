from abc import ABCMeta
from uuid import UUID

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.sale import CreateSaleRequest

class SalesService(metaclass=ABCMeta):
    """
            Default class for sale service implementation
        """

    def create(self, user_id: UUID, email: str, sale: CreateSaleRequest) -> BaseResponse:
        """make a sale"""
        raise NotImplementedError

    def verify_payment(self, reference: str) -> BaseResponse:
        """verify payment"""
        raise NotImplementedError