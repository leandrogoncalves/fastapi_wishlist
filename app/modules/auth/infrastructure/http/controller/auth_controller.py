from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Auth"]
)


@router.get("/auth")
async def handle_auth():
    return [{'id': 1}]
