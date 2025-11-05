from typing import List, Optional

from pydantic import UUID4, BaseModel

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.stock_entry import GetStockResponse


class CreateProduct(BaseModel):
    name: str
    description: str
    image: str

class CreateProductResponse(BaseResponse):
    name: str
    description: str
    image: str

class UpdateProduct(BaseModel):
    description: str
    image: Optional[str] = None

class GetProduct(BaseModel):
    id: UUID4

class GetResponse(BaseResponse):
    id: UUID4
    name: str
    description: str
    image: Optional[str] = None
    stock_items: Optional[List[GetStockResponse]] = None

class List(BaseResponse):
    products: List[GetResponse]