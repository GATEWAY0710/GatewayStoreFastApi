from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, UUID4

from application.use_case.models.base_response import BaseResponse


class SalesReport(BaseResponse):
    total_sales: Decimal
    period: str


class ProfitLossReport(BaseResponse):
    total_revenue: Decimal
    total_cost: Decimal
    net_profit: Decimal
    period: str


class SalesStatusReport(BaseResponse):
    successful_sales: int
    unsuccessful_sales: int


class ProductPerformance(BaseModel):
    product_id: UUID4
    product_name: str
    units_sold: int


class ProductPerformanceReport(BaseResponse):
    highest_sold: Optional[ProductPerformance] = None
    lowest_sold: Optional[ProductPerformance] = None


class LowStockAlert(BaseModel):
    product_id: UUID4
    product_name: str
    total_remaining_quantity: int

class LowStockReport(BaseResponse):
    alerts: List[LowStockAlert]