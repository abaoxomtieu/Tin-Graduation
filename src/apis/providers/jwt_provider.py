from typing import AnyStr, Dict, Union
import os
from fastapi import HTTPException, status
from jose import jwt, JWTError


class JWTProvider:
    """
    Perform JWT Encryption and Decryption
    """

    def __init__(
        self, secret: AnyStr = os.environ.get("JWT_SECRET"), algorithm: AnyStr = "HS256"
    ):
        self.secret = secret
        self.algorithm = algorithm

    def encrypt(self, data: Dict) -> AnyStr:
        """
        Encrypt the data with JWT
        """
        return jwt.encode(data, self.secret, algorithm=self.algorithm)

    def decrypt(self, token: AnyStr) -> Union[Dict, None]:
        """
        Decrypt the token with JWT
        """
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials. {str(e)}",
            )


jwt_provider = JWTProvider()
