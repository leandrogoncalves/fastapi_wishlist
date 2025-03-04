from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from modules.core.config.auth import authenticate, create_access_token
from modules.core.config.database import get_session


router = APIRouter(
    prefix="/api",
    tags=["Auth"]
)


@router.post("/auth/login",
    description="Customer authentication",
    summary="Login",
)
async def handle_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    customer = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not customer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return JSONResponse(
        content={
            "access_token": create_access_token(subject=customer.id),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK
    )
