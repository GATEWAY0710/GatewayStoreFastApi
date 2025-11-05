from datetime import datetime
from logging import Logger

from decimal import Decimal
from typing import Tuple, List

from sqlalchemy import select, func, and_
from sqlalchemy.exc import SQLAlchemyError
from application.persistence.report_repo import ReportRepository as DefaultReportRepository
from domain.models import Sale, SaleItem, Product,StockEntry
from infrastructure.database import SessionLocal

class ReportRepository(DefaultReportRepository):
    _logger: Logger
    def __init__(self, logger: Logger):
        self._logger = logger

    def get_total_sales(self, start_date: datetime, end_date: datetime) -> Decimal:
        with SessionLocal() as session:
            try:
                statement = select(func.sum(Sale.total_amount)).where(
                    and_(Sale.paid == True, Sale.sale_date.between(start_date, end_date))
                )
                total = session.scalars(statement).one_or_none()
                return total or Decimal(0)
            except SQLAlchemyError as e:
                self._logger.error(f"database error: {e}")
                return Decimal(0)
            except Exception as e:
                self._logger.error(f"error getting details: {e}")
                return Decimal(0)


    def get_profit_loss(self, start_date: datetime, end_date: datetime) -> Tuple[Decimal, Decimal]:
        with SessionLocal() as session:
            try:
                statement = select(func.sum(SaleItem.sale_price * SaleItem.quantity),
                                   func.sum(StockEntry.cost_price * SaleItem.quantity)).join(
                    Sale, SaleItem.sale_id == Sale.id)\
                    .join(Product, SaleItem.product_id == Product.id)\
                    .join(StockEntry, Product.id == StockEntry.product_id)\
                    .where(and_(Sale.paid == True, Sale.sale_date.between(start_date, end_date)))

                result = session.execute(statement).first()
                revenue = result[0] or Decimal(0)
                cost = result[1] or Decimal(0)
                return revenue, cost
            except SQLAlchemyError as e:
                self._logger.error(f"database error: {e}")
                return Decimal(0), Decimal(0)
            except Exception as e:
                self._logger.error(f"error getting details: {e}")
                return Decimal(0), Decimal(0)

    def get_sales_status_counts(self) -> Tuple[int, int]:
        with SessionLocal() as session:
            try:
                successful_stmt = select(func.count(Sale.id)).where(Sale.paid == True)
                unsuccessful_stmt = select(func.count(Sale.id)).where(Sale.paid == False)
                successful_count = session.scalars(successful_stmt).one_or_none()
                unsuccessful_count = session.scalars(unsuccessful_stmt).one_or_none()
                return successful_count, unsuccessful_count
            except SQLAlchemyError as e:
                self._logger.error(f"database error: {e}")
                return 0,0
            except Exception as e:
                self._logger.error(f"error getting details: {e}")
                return 0,0


    def get_product_performance(self) -> List[Tuple[str, str, int]]:
        with SessionLocal() as session:
            try:
                statement = select(
                    Product.id, Product.name, func.sum(SaleItem.quantity).label("total_sold")
                ).join(Product, SaleItem.product_id == Product.id)\
                .group_by(Product.id, Product.name).order_by(func.sum(SaleItem.quantity).desc())
                return session.execute(statement).all()
            except SQLAlchemyError as e:
                self._logger.error(f"database error: {e}")
                return []
            except Exception as e:
                self._logger.error(f"error getting details: {e}")
                return []

    def get_low_stock_products(self, threshold: int) -> List[Tuple[str, str, int]]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(
                        Product.id,
                        Product.name,
                        func.sum(StockEntry.remaining_quantity).label("total_remaining")
                    )
                    .join(StockEntry, Product.id == StockEntry.product_id)
                    .group_by(Product.id, Product.name)
                    .having(func.sum(StockEntry.remaining_quantity) <= threshold)
                )
                return session.execute(statement).all()
            except SQLAlchemyError as e:
                self._logger.error(f"database error: {e}")
                return []
            except Exception as e:
                self._logger.error(f"error getting details: {e}")
                return []
