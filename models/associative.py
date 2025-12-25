from sqlalchemy import Table, Column, ForeignKey

from models import Base


products_categories = Table(
    "products_categories",
        Base.metadata,
        Column("products", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
        Column("categories", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    )