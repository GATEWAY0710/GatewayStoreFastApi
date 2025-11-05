from abc import ABCMeta
from typing import Optional, List
from uuid import UUID

from domain.models import Product


class ProductRepository(metaclass=ABCMeta):
    """
        Default class for product repository implementation
    """

    def create(self, product: Product) -> Optional[Product]:
        """create product"""
        raise NotImplementedError

    def update(self, product: Product) -> Optional[Product]:
        """update product"""
        raise NotImplementedError

    def get(self, id: UUID) -> Optional[Product]:
        """get product"""
        raise NotImplementedError

    def get_by_name(self, name: str) -> Optional[Product]:
        """get product by name"""
        raise NotImplementedError

    def list(self) -> List[Product]:
        """list product"""
        raise NotImplementedError