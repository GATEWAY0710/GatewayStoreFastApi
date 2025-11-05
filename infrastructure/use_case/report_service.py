from datetime import datetime, timedelta
from decimal import Decimal
from logging import Logger
from typing import Optional, Tuple

from application.persistence.report_repo import ReportRepository
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.report import SalesReport, ProfitLossReport, SalesStatusReport, \
    ProductPerformanceReport, ProductPerformance, LowStockAlert, LowStockReport
from application.use_case.report_service import ReportService as DefaultReportService


class ReportService(DefaultReportService):
    _logger: Logger
    report_repository: ReportRepository

    def __init__(self, logger: Logger, report_repository: ReportRepository):
        self._logger = logger
        self._report_repository = report_repository

    def _get_date_range(self, year: int, month: Optional[int] = None, day: Optional[int] = None):
        self._logger.info("getting date range")
        if day and month:
            start_date = datetime(year=year, month=month, day=day)
            end_date = start_date + timedelta(days=1)
            period_str = start_date.strftime("%Y-%m-%d")
        elif month:
            start_date = datetime(year=year, month=month, day=1)
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day -  1)
            period_str = start_date.strftime("%Y-%m")
        else:
            start_date = datetime(year=year, month=1, day=1)
            end_date = datetime(year + 1, month=1, day=1)
            period_str = str(year)
        return start_date, end_date, period_str


    def get_sales_report(self, year: int, month: Optional[int] = None, day: Optional[int] = None) -> BaseResponse:
        start_date, end_date, period_str = self._get_date_range(year, month, day)
        self._logger.info("getting sales report")
        total_sales = self._report_repository.get_total_sales(start_date=start_date, end_date=end_date)
        if total_sales == 0:
            self._logger.info("no sales found for that period")
        self._logger.info(f"total sales: {total_sales}")
        response = SalesReport(status=True, total_sales=total_sales, period=period_str)
        response._status_code = 200
        return response


    def get_product_performance_report(self) -> BaseResponse:
        self._logger.info("getting product performance report")
        performance_data = self._report_repository.get_product_performance()
        if not performance_data:
            self._logger.info("no product performance data")
            response = BaseResponse(status=True, message="no product performance data")
            response._status_code = 200
            return response
        self._logger.info("product performance data: {}".format(performance_data))
        highest_sold = ProductPerformance(product_id=performance_data[0][0], product_name=performance_data[0][1], units_sold=performance_data[0][2])
        lowest_sold = ProductPerformance(product_id=performance_data[-1][0], product_name=performance_data[-1][1], units_sold=performance_data[-1][2])
        response = ProductPerformanceReport(status=True, highest_sold=highest_sold, lowest_sold=lowest_sold)
        response._status_code = 200
        return response


    def get_low_stock_alerts(self, threshold: int) -> BaseResponse:
        self._logger.info("getting low stock alerts")
        low_stock_products = self._report_repository.get_low_stock_products(threshold=threshold)
        response = [
            LowStockAlert(product_id=p[0], product_name=p[1], total_remaining_quantity=p[2])
            for p in low_stock_products
        ]
        if not response:
            self._logger.info("no low stock alerts")
            response = LowStockReport(status=True, message="all products sufficiently stocked", alerts=[])
            response._status_code = 200
            return response

        self._logger.info("low stock alerts: {}".format(low_stock_products))
        response = LowStockReport(status=True, alerts=response)
        response._status_code = 200
        return response


    def get_profit_loss_report(self, year: int, month: Optional[int] = None, day: Optional[int] = None) -> BaseResponse:
        start_date, end_date, period_str = self._get_date_range(year, month, day)
        total_revenue, total_cost = self._report_repository.get_profit_loss(start_date=start_date, end_date=end_date)
        self._logger.info("profit loss report: {}".format(total_revenue))
        net_profit = total_revenue - total_cost
        if total_revenue == 0 and total_cost == 0:
            response = ProfitLossReport(status=True, net_profit=Decimal(0), total_revenue=Decimal(0), total_cost=Decimal(0), period=period_str, message="no profit/loss for the selected period")
            response._status_code = 200
            return response
        response = ProfitLossReport(status=True, total_revenue=total_revenue, total_cost=total_cost, period=period_str, net_profit=net_profit)
        response._status_code = 200
        return response


    def get_sales_status_report(self) -> BaseResponse:
        self._logger.info("getting sales status report")
        successful, unsuccessful = self._report_repository.get_sales_status_counts()
        response = SalesStatusReport(status=True, successful_sales=successful, unsuccessful_sales=unsuccessful)
        response._status_code = 200
        return response