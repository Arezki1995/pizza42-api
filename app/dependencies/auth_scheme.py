"""
JWT Authentication scheme dependency definition
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List

from app.security.jwt import VerifyJWT

auth_token_scheme = HTTPBearer()


def jwt_required(scopes: List[str] , permissions: Optional[List[str]] = None):
    def dependency( token: HTTPAuthorizationCredentials = Depends(auth_token_scheme) ) -> dict:
        verifier = VerifyJWT(
            token=token.credentials,
            scopes=scopes,
            permissions=permissions,
        )

        result = verifier.verify()

        # print verification result for DEBUG
        print("JWT Verification result: ", result)

        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"{result.get('type')} - {result.get('payload')}",
            )

        return result["payload"]  # return decoded JWT payload

    return dependency
