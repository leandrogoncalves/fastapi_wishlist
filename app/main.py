from modules.core.config import env, dependencies
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from modules.core.infrastructure.http.api import health_controller
from modules.auth.infrastructure.http.api import auth_controller
from modules.product.infrastructure.http.api import product_controller
from modules.customer.infrastructure.http.api import customer_controller
from modules.wishlist.infrastructure.http.api import wishlist_controller

app = FastAPI(
    redirect_slashes=False,
    name=env.APP_NAME,
    title=env.APP_TITLE,
    description=env.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[env.CORS_ALLOW_ORIGINS],
    allow_credentials=env.CORS_ALLOW_CREDENTIALS,
    allow_methods=[env.CORS_ALLOW_METHODS],
    allow_headers=[env.CORS_ALLOW_HEADERS],
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
        host=env.APP_HOST,
        port=env.APP_PORT,
        log_level=env.APP_LOG_LEVEL,
        reload=env.APP_RELOAD
    )