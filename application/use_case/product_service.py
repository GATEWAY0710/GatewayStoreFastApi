from abc import ABCMeta
from uuid import UUID

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.product import CreateProduct, UpdateProduct


class ProductService(metaclass=ABCMeta):
    """
        Default class for product service implementation
    """

    def create(self, product: CreateProduct) -> BaseResponse:
        """create product"""
        raise NotImplementedError


    def update(self, name: str, product: UpdateProduct) -> BaseResponse:
        """update product"""
        raise NotImplementedError

    def get(self, id: UUID) -> BaseResponse:
        """get product"""
        raise NotImplementedError

    def get_by_name(self, name: str) -> BaseResponse:
        """get product by name"""
        raise NotImplementedError

    def list(self) -> BaseResponse:
        """list product"""
        raise NotImplementedError