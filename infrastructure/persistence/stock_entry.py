from logging import Logger
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from domain.models import StockEntry
from infrastructure.database import SessionLocal
from application.persistence.stock_entry import StockEntryRepository as DefaultStockRepository
class StockEntryRepository(DefaultStockRepository):
    _logger: Logger
    def __init__(self, logger:Logger):
        self._logger = logger

    def create(self,product_name: str, stock_entry: StockEntry) -> Optional[StockEntry]:
        with SessionLocal() as session:
            try:
                session.add(stock_entry)
                self._logger.info(f"adding stocks for {product_name}")
                session.commit()
                session.refresh(stock_entry)
                return stock_entry
            except SQLAlchemyError as e:
                self._logger.error(f"database error in adding {stock_entry.quantity} quantity to {product_name}, {e} ")
                return None
            except Exception as e:
                self._logger.error(f"an error occured, {e}")
                return None

    def update(self, id: UUID, stock_entry: StockEntry) -> Optional[StockEntry]:
        with SessionLocal() as session:
            try:
                statement = (select(StockEntry).where(StockEntry.id == id))
                update = session.scalars(statement).one_or_none()
                if not update:
                    return None

                update.cost_price = stock_entry.cost_price
                update.selling_price = stock_entry.selling_price
                update.quantity = stock_entry.quantity

                session.commit()
                session.refresh(update)
                return update
            except SQLAlchemyError as e:
                self._logger.error(f"database error in updating {stock_entry.id}, {e}")
                return None
            except Exception as e:
                self._logger.error(f"error in updating product stock, {e}")
                return None


    def get(self, id: UUID) -> Optional[StockEntry]:
        with SessionLocal() as session:
            try:
                statement = (select(StockEntry).options(selectinload(StockEntry.product)).where(StockEntry.id == str(id)))
                stock = session.scalars(statement).one_or_none()
                return stock

            except SQLAlchemyError as e:
                self._logger.error(f"database error in getting stock{e}")
                return None
            except Exception as e:
                self._logger.error(f"error getting stock{e}")
                return None


    def list(self) -> List[StockEntry]:
        with SessionLocal() as session:
            try:
                statement = (select(StockEntry).options(selectinload(StockEntry.product)))
                return list(session.scalars(statement).all())
            except SQLAlchemyError as e:
                self._logger.error(f"unable to fetch list of stocks from database{e}")
                return []
            except Exception as e:
                self._logger.error(f"unable to get list of stocks: {e}")
                return []

    def reduce_stock_for_sales(self, entries_to_reduce: List[StockEntry]) -> bool:

        with SessionLocal() as session:
            try:
                for entry in entries_to_reduce:
                    session.merge(entry)

                session.commit()
                return True
            except SQLAlchemyError as e:
                self._logger.error(f"Database error during stock reduction: {e}")
                return False
            except Exception as e:
                self._logger.error(f"Unexpected error during stock reduction: {e}")
                return False