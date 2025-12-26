from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum
from sqlalchemy import Boolean, false, Text
from enum import Enum as PyEnum


class Base(DeclarativeBase):
    pass


class ProductStatus(PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus, name='product_status'),
        nullable=False,
        server_default=ProductStatus.DRAFT.value
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                              server_default=false())
    description: Mapped[str] = mapped_column(Text, nullable=False)
