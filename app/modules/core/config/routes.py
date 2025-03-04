from fastapi import APIRouter
from modules.core.infrastructure.http.controller import health_controller
from modules.auth.infrastructure.http.controller import auth_controller
from modules.product.infrastructure.http.controller import product_controller
from modules.customer.infrastructure.http.controller import customer_controller
from modules.wishlist.infrastructure.http.controller import wishlist_controller

api_router = APIRouter()

api_router.include_router(health_controller.router)
api_router.include_router(auth_controller.router)
api_router.include_router(product_controller.router)
api_router.include_router(customer_controller.router)
api_router.include_router(wishlist_controller.router)