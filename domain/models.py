from __future__ import annotations

import datetime
from typing import List, Optional
from uuid import UUID as UUID_T, uuid4

from sqlalchemy import (
    CHAR, Column, String, DateTime, Enum, ForeignKey, Table, Index, UniqueConstraint, func, Integer, Float, Boolean, Numeric
)
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, declarative_base
)
from domain.enums.role import Role as DomainRole

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __tablename__: str = None

    id: Mapped[UUID_T] = mapped_column(CHAR(36), primary_key=True, default=uuid4)
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    modified_by: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(50))
    hash_salt: Mapped[str] = mapped_column(String(1000), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(1000), nullable=False)
    role: Mapped[DomainRole] = mapped_column(Enum(DomainRole), nullable=False, default=DomainRole.Customer)

    sales: Mapped[List["Sale"]] = relationship("Sale", back_populates="customer")
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(BaseModel):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("users.id"), unique=True, nullable=False)

    user: Mapped[User] = relationship(back_populates="profile")



class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(1000))

    stock_entries: Mapped[List["StockEntry"]] = relationship(
        back_populates="product", cascade="all, delete-orphan", lazy="selectin"
    )

class StockEntry(BaseModel):
    __tablename__ = "stock_entries"

    product_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("products.id"), nullable=False)
    cost_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    selling_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    product: Mapped["Product"] = relationship(back_populates="stock_entries")


class Sale(BaseModel):
    __tablename__ = "sales"

    customer_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False)
    sale_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), unique=True)

    customer: Mapped["User"] = relationship("User", back_populates="sales")
    items: Mapped[List["SaleItem"]] = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(BaseModel):
    __tablename__ = "sale_items"

    sale_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("sales.id"), nullable=False)
    product_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


