from abc import ABCMeta
from typing import Optional, List
from uuid import UUID

from domain.models import Product, Sale, SaleItem

class SalesRepository(metaclass=ABCMeta):
    """Default class for sale repository implementation"""

    def create(self, sale: Sale) -> Optional[Sale]:
        """Create a new sale"""
        raise NotImplementedError

    def get_by_reference(self, reference: str) -> Optional[Sale]:
        """Get a sale by reference"""
        raise NotImplementedError

    def update(self, sale: Sale) -> Optional[Sale]:
        """Confirm payment"""
        raise NotImplementedError