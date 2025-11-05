from decimal import Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel

from application.use_case.models.base_response import BaseResponse

class CreateStock(BaseModel):
    quantity: int
    cost_price: Decimal
    selling_price: Decimal

class CreateStockResponse(BaseResponse):
    quantity: int
    cost_price: Decimal
    selling_price: Decimal

class UpdateStock(BaseModel):
    cost_price: Decimal
    selling_price: Decimal

class UpdateStockResponse(BaseResponse):
    cost_price: Decimal
    selling_price: Decimal

class GetStockResponse(BaseResponse):
    quantity: int
    remaining_quantity: int
    cost_price: Decimal
    selling_price: Decimal
    added_date: str

class ListStocks(BaseResponse):
    stocks: List[GetStockResponse]