from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from http import HTTPStatus
from datetime import datetime

router = APIRouter(
    tags=["Health"]
)

@router.get("/", include_in_schema=False)
async def health():
    return RedirectResponse(url="/health")


@router.get("/health")
async def health():
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "message": "Healthy",
            "time": datetime.now().strftime("%m-%d-%YT%H:%M:%S"),
            "docs": '/docs'
        }
    )