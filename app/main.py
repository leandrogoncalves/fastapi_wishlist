import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    redirect_slashes=False,
    name='FastApi_whishlist',
    description='Projeto para teste de habilidades de programação',
    docs_url=f"/{config.SWAGGER_URL}"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Welcome to the FastAPI wishlist application!"}