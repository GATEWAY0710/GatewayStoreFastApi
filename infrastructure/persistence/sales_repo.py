from logging import Logger
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from application.persistence.sales_repo import SalesRepository as DefaultSaleRepository
from domain.models import Sale
from infrastructure.database import SessionLocal

class SalesRepository(DefaultSaleRepository):
    _logger: Logger

    def __init__(self, logger:Logger):
        self._logger = logger

    def create(self, sale: Sale) -> Optional[Sale]:
        with SessionLocal() as session:
            try:
                session.add(sale)
                session.commit()
                session.refresh(sale)
                return sale
            except SQLAlchemyError as e:
                self._logger.error(f"database error in creating sale: {e}")
                return None
            except Exception as e:
                self._logger.error(f"error in creating sale: {e}")
                return None


    def get_by_reference(self, reference: str) -> Optional[Sale]:
        with SessionLocal() as session:
            try:
                statement = select(Sale).where(Sale.payment_reference==reference).options(selectinload(Sale.items))
                sale = session.scalars(statement).one_or_none()
                return sale
            except SQLAlchemyError as e:
                self._logger.error(f"database error in getting sale: {e}")
                return None
            except Exception as e:
                self._logger.error(f"error in getting sale: {e}")
                return None



    def update(self, sale: Sale) -> Optional[Sale]:
        with SessionLocal() as session:
            try:
                session.add(sale)
                session.commit()
                session.refresh(sale)
                return sale
            except SQLAlchemyError as e:
                self._logger.error(f"database error in confirming sale payment: {e}")
                return None
            except Exception as e:
                self._logger.error(f"error in confirming sale payment: {e}")
                return None