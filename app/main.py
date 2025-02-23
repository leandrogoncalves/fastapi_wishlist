from config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from modules.core.infrastructure.http.api import health_controller
from modules.auth.infrastructure.http.api import auth_controller
from modules.product.infrastructure.http.api import product_controller
from modules.customer.infrastructure.http.api import customer_controller
from modules.wishlist.infrastructure.http.api import wishlist_controller

app = FastAPI(
    redirect_slashes=False,
    name=settings.APP_NAME,
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ALLOW_ORIGINS],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=[settings.CORS_ALLOW_METHODS],
    allow_headers=[settings.CORS_ALLOW_HEADERS],
)

app.include_router(health_controller.router)
app.include_router(auth_controller.router)
app.include_router(product_controller.router)
app.include_router(customer_controller.router)
app.include_router(wishlist_controller.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.APP_LOG_LEVEL,
        reload=settings.APP_RELOAD
    )