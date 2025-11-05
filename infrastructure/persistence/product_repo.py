from logging import Logger
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from infrastructure.database import SessionLocal
from application.persistence.product_repo import ProductRepository as DefaultProductRepository
from domain.models import Product


class ProductRepository(DefaultProductRepository):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    def create(self, product: Product) -> Optional[Product]:
        with SessionLocal() as session:
            try:
                session.add(product)
                self._logger.info(f"product {product.name} created successfully")
                session.commit()
                session.refresh(product)
                return product
            except SQLAlchemyError as e:
                self._logger.error(f"Database error while creating product with id {product.name}: {e}")
                return None
            except Exception as e:
                self._logger.error(f"an error occured while cxreating product, {e}")
                return None


    def update(self, name: str, product: Product) -> Optional[Product]:
        with SessionLocal() as session:
            try:
                statement = (select(Product).where(Product.name == name))
                update = session.scalars(statement).one_or_none()
                if not update:
                    return None
                update.description = product.description
                update.image = product.image

                session.commit()
                session.refresh(update)
                return update
            except SQLAlchemyError as e:
                self._logger.error(f"Database error while updating product with id {id}: {e}")
                return None
            except Exception as e:
                self._logger.error(f"unable to update product {product.name}, {e}")
                return None


    def get(self, id: UUID) -> Optional[Product]:
        with SessionLocal() as session:
            try:
                statement = (select(Product).options(selectinload(Product.stock_entries)).where(Product.id == str(id)))
                product = session.scalars(statement).one_or_none()
                return product
            except SQLAlchemyError as e:
                self._logger.error(f"Database error while fetching product with id {id}: {e}")
                return None
            except Exception as e:
                self._logger.error(f"An unexpected error occurred while fetching product {id}: {e}")
                return None

    def get_by_name(self, name: str) -> Optional[Product]:
        with SessionLocal() as session:
            try:
                statement = (select(Product).options(selectinload(Product.stock_entries)).where(Product.name == name))
                product = session.scalars(statement).one_or_none()
                return product
            except SQLAlchemyError as e:
                self._logger.error(f"Database error while fetching product with id {name}: {e}")
                return None
            except Exception as e:
                self._logger.error(f"An unexpected error occurred while fetching product {name}: {e}")
                return None

    def list(self) -> List[Product]:
        with SessionLocal() as session:
            try:
                statement = (select(Product).options(selectinload(Product.stock_entries)))
                return list(session.scalars(statement).all())
            except SQLAlchemyError as e:
                self._logger.error(f"Database error while listing products: {e}")
                return []
            except Exception as e:
                self._logger.error(f"An unexpected error occurred while listing products: {e}")
                return []