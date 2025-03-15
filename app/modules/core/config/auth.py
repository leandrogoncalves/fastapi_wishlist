from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr, BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from .settings import settings
from .security import check_password
from .database import get_session
from modules.customer.infrastructure.database.models.customer_model import CustomerModel


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/auth/login"
)


class TokenData(BaseModel):
    username: Optional[str] = None


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[CustomerModel]:
    async with db as session:
        query = select(CustomerModel).filter(CustomerModel.email == email)
        result = await session.execute(query)
        customer: CustomerModel = result.scalars().unique().one_or_none()

        if not customer:
            return None

        if not check_password(password, customer.password):
            return None

        return customer


def _create_token(token_type: str, lifetime: timedelta, subject: str) -> str:
    # https://datatracker.ietf.org/doc/rfc7519/
    payload = {}
    local_timezone = timezone('America/Sao_Paulo')
    payload['type'] = token_type
    payload['exp'] = datetime.now(tz=local_timezone) + lifetime
    payload['iat'] = datetime.now(tz=local_timezone)
    payload['sub'] = str(subject)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(subject: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subject=subject
    )


async def get_current_customer(
        db: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_schema)
) -> CustomerModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception

    async with db as session:
        query = select(CustomerModel).filter(CustomerModel.id == token_data.username)
        result = await session.execute(query)
        customer: CustomerModel = result.scalars().unique().one_or_none()

        if customer is None:
            raise credential_exception

        return customer
