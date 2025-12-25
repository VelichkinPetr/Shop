from fastapi import APIRouter
from api.routers.v1 import *


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
api_router.include_router(category_router, prefix="/categories", tags=["categories"])
api_router.include_router(cart_router, prefix="/cart", tags=["cart"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
