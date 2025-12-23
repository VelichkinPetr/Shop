from .auth import router as auth_router
from .user import router as user_router
from .product import router as product_router
from .category import router as category_router
from .cart import router as cart_router
from .order import router as order_router

__all__ = [
    'auth_router',
    'user_router',
    'product_router',
    'category_router',
    'cart_router',
    'order_router'
]