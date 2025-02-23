import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from modules.core.infrastructure.http.api import health_controller
from modules.auth.infrastructure.http.api import auth_controller
from modules.product.infrastructure.http.api import product_controller
from modules.customer.infrastructure.http.api import customer_controller
from modules.wishlist.infrastructure.http.api import wishlist_controller

app = FastAPI(
    redirect_slashes=False,
    name=config.APP_NAME,
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.CORS_ALLOW_ORIGINS],
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=[config.CORS_ALLOW_METHODS],
    allow_headers=[config.CORS_ALLOW_HEADERS],
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
        host=config.APP_HOST,
        port=config.APP_PORT,
        log_level=config.APP_LOG_LEVEL,
        reload=config.APP_RELOAD
    )