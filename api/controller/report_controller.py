from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.token import get_current_user, allowed_roles
from application.use_case.models.auth import TokenData
from application.use_case.models.report import SalesReport, ProfitLossReport, SalesStatusReport, \
    ProductPerformanceReport, LowStockAlert, LowStockReport
from infrastructure.dependency import Container

router = APIRouter()

@router.get("", response_model=SalesReport)
def sales_report(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))],year: int, month: Optional[int] = None, day: Optional[int] = None, ):
    report_service = Container.report_service()
    response = report_service.get_sales_report(year=year, month=month, day=day)
    if not response.status:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response


@router.get("/profit-loss", response_model=ProfitLossReport)
def profit_loss_report(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))],year: int, month: Optional[int] = None, day: Optional[int] = None ):
    report_service = Container.report_service()
    response = report_service.get_profit_loss_report(year=year, month=month, day=day)
    if not response.status:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response


@router.get("/sales-status", response_model=SalesStatusReport)
def Sales_status_report(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    report_service = Container.report_service()
    response = report_service.get_sales_status_report()
    if not response.status:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response


@router.get("/product-performance", response_model=ProductPerformanceReport)
def product_performance_report(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    report_service = Container.report_service()
    response = report_service.get_product_performance_report()
    if not response.status:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response


@router.get("/low-stock-alert", response_model=LowStockReport)
def low_stock_alert(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    report_service = Container.report_service()
    response = report_service.get_low_stock_alerts(threshold=5)
    if not response.status:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response