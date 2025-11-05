from abc import ABCMeta, abstractmethod
from typing import Optional

from application.use_case.models.base_response import BaseResponse


class ReportService(metaclass=ABCMeta):
    """default report service implementation"""

    def get_sales_report(self, year: int, month: Optional[int] = None, day: Optional[int] = None) -> BaseResponse:
        """get sales report"""
        raise NotImplementedError

    def get_profit_loss_report(self, year: int, month: Optional[int] = None, day: Optional[int] = None) -> BaseResponse:
        """get profit or loss report"""
        raise NotImplementedError

    def get_sales_status_report(self) -> BaseResponse:
        """get sales status report"""
        raise NotImplementedError

    def get_product_performance_report(self) -> BaseResponse:
        """get product performance report"""
        raise NotImplementedError

    def get_low_stock_alerts(self, threshold: int) -> BaseResponse:
        """get low stock alerts"""
        raise NotImplementedError