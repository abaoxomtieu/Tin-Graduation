from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from src.apis.providers.jwt_provider import jwt_provider as jwt
from bson import ObjectId
from jose import JWTError
from src.utils.logger import logger
import requests

security = HTTPBearer()

import jwt


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):

    try:
        token = credentials.credentials
        if not token:
            return JSONResponse(
                content={"msg": "Authentication failed"}, status_code=401
            )
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("userId")
        role = payload.get("role")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        url = "http://103.81.87.99:8080/identity/auth/introspect"
        headers = {"accept": "*/*", "Content-Type": "application/json"}
        payload = {"token": token}
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        if not result.get("data").get("valid"):
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "role": role}
    except JWTError:
        return JSONResponse(content={"msg": "Authentication failed"}, status_code=401)
