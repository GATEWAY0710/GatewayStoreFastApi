from abc import ABCMeta
from datetime import datetime
from decimal import Decimal
from typing import  List, Tuple


class ReportRepository(metaclass=ABCMeta):
    """
        default class Report repository.
    """

    def get_total_sales(self, start_date: datetime, end_date: datetime) -> Decimal:
        """get total sales"""
        raise NotImplementedError

    def get_profit_loss(self, start_date: datetime, end_date: datetime) -> Tuple[Decimal, Decimal]:
        """get profit or loss"""
        raise NotImplementedError

    def get_sales_status_counts(self) -> Tuple[int, int]:
        """get sales status counts"""
        raise NotImplementedError

    def get_product_performance(self) -> List[Tuple[str, str, int]]:
        """get product performance"""
        raise NotImplementedError

    def get_low_stock_products(self, threshold: int) -> List[Tuple[str, str, int]]:
        """get low stock products"""
        raise NotImplementedError