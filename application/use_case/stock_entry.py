from abc import ABCMeta
from uuid import UUID

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.stock_entry import CreateStock, UpdateStock


class StockEntryService(metaclass=ABCMeta):
    """
        Default class for stock entry service implementation
    """
    def create(self, product_name: str, stock_entry: CreateStock) -> BaseResponse:
        """add stock to product"""
        raise NotImplementedError

    def update(self,id: UUID, stock_entry: UpdateStock) -> BaseResponse:
        """update stock in product"""
        raise NotImplementedError

    def get(self, id: UUID) -> BaseResponse:
        """get stock of product"""
        raise NotImplementedError

    def list(self) -> BaseResponse:
        """list stocks of all product"""
        raise NotImplementedError
