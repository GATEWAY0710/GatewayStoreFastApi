from urllib import response
from uuid import UUID

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.stock_entry import CreateStockResponse, CreateStock, UpdateStockResponse, UpdateStock, \
    GetStockResponse, ListStocks
from infrastructure.dependency import Container
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("", response_model=CreateStockResponse)
def create(product_name: str, stock_entry: CreateStock) -> BaseResponse:
    stock_entry_service = Container.stock_entry_service()
    response = stock_entry_service.create(product_name=product_name, stock_entry=stock_entry)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.put("", response_model=UpdateStockResponse)
def update(id: str, stock_entry: UpdateStock) -> BaseResponse:
    stock_entry_service = Container.stock_entry_service()
    response = stock_entry_service.update(id=id, stock_entry=stock_entry)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{id}", response_model=GetStockResponse)
def get(id: UUID) -> BaseResponse:
    stock_entry_service = Container.stock_entry_service()
    response = stock_entry_service.get(id=id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("", response_model=ListStocks)
def list() -> BaseResponse:
    stock_entry_service = Container.stock_entry_service()
    response = stock_entry_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response