from abc import ABCMeta
from typing import Optional, List
from uuid import UUID
from domain.models import StockEntry

class StockEntryRepository(metaclass=ABCMeta):
    """
        Default class for stock entry repository implementation
    """

    def create(self,product_name: str,stock_entry: StockEntry) -> Optional[StockEntry]:
        """add stock to product"""
        raise NotImplementedError

    def update(self, id: UUID, stock_entry: StockEntry) -> Optional[StockEntry]:
        """update stock in product"""
        raise NotImplementedError

    def get(self, id: UUID) -> Optional[StockEntry]:
        """get stock in product"""
        raise NotImplementedError

    # def get_by_product_name(self, name: str) -> Optional[StockEntry]:
    #     """get stock in product by name"""
    #     raise NotImplementedError

    def list(self) -> List[StockEntry]:
        """list stock in product"""
        raise NotImplementedError

    def reduce_stock_for_sales(self, entries_to_reduce: List[StockEntry]) -> bool:
        """reduce stock for sales"""
        raise NotImplementedError