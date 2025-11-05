from typing import List
from pydantic import BaseModel, UUID4
from application.use_case.models.base_response import BaseResponse

class SaleItemRequest(BaseModel):
    product_id: UUID4
    quantity: int

class CreateSaleRequest(BaseModel):
    items: List[SaleItemRequest]

class CreateSaleResponse(BaseResponse):
    authorization_url: str
    access_code: str
    reference: str

class VerifySaleResponse(BaseResponse):
    sale_id: UUID4
    payment_status: str