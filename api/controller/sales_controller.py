from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from api.token import get_current_user
from application.use_case.models.auth import TokenData
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.sale import CreateSaleRequest, CreateSaleResponse, VerifySaleResponse
from application.use_case.sales_service import SalesService
from infrastructure.dependency import Container

router = APIRouter()

@router.post("", response_model=CreateSaleResponse)
def create(sale: CreateSaleRequest, current_user: Annotated[TokenData, Depends(get_current_user)]) -> BaseResponse:
    sale_service = Container.sales_service()
    response = sale_service.create(user_id=current_user.user_id, sale=sale, email=current_user.email)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response


@router.get("/verify/{reference}", response_model=VerifySaleResponse)
def verify_payment(reference: str) -> BaseResponse:
    sales_service = Container.sales_service()
    response = sales_service.verify_payment(reference=reference)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response
