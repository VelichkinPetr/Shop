from sqlalchemy import Table, Column, ForeignKey

from models import Base


products_categories = Table(
    "products_categories",
        Base.metadata,
        Column("products", ForeignKey("products.id"), primary_key=True),
        Column("categories", ForeignKey("categories.id"), primary_key=True),
    )