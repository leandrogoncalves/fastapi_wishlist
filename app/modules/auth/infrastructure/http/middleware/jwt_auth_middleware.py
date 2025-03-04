from jose import jwt, JWTError
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from sqlalchemy.future import select
from modules.core.config.settings import settings
from modules.core.config.database import get_session
from modules.customer.infrastructure.database.models.customer_model import CustomerModel


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in ["/api/auth/login", "/docs", "/openapi.json", "/health"]:
            return await call_next(request)

        credential_exception: HTTPException = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        auth: str = request.headers.get("authorization")
        if not auth:
            return JSONResponse(
                content={"error": "Not authenticated"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme."
                )
        except ValueError:
            return JSONResponse(
                content={"detail": "Invalid authorization header"},
                status_code=status.HTTP_401_UNAUTHORIZED
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

        except JWTError:
            return JSONResponse(
                content={"detail": "Invalid token"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        async with get_session() as session:
            query = select(CustomerModel).filter(CustomerModel.id == username)
            result = await session.execute(query)
            customer: CustomerModel = result.scalars().unique().one_or_none()

            if customer is None:
                raise credential_exception

            request.state.user = customer

        response = await call_next(request)
        return response