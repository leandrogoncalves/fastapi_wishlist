from modules.core.config import env, dependencies
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from modules.core.config.routes import api_router
from modules.auth.infrastructure.http.middleware.jwt_auth_middleware import JWTAuthMiddleware


@asynccontextmanager
async def lifspan(app: FastAPI):
    print('starting')
    yield
    print('stopping')

app = FastAPI(
    redirect_slashes=False,
    name=env.APP_NAME,
    title=env.APP_TITLE,
    description=env.APP_DESCRIPTION,
    lifespan=lifspan
)

app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[env.CORS_ALLOW_ORIGINS],
    allow_credentials=env.CORS_ALLOW_CREDENTIALS,
    allow_methods=[env.CORS_ALLOW_METHODS],
    allow_headers=[env.CORS_ALLOW_HEADERS],
)

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host=env.APP_HOST,
        port=env.APP_PORT,
        log_level=env.APP_LOG_LEVEL,
        reload=env.APP_RELOAD
    )