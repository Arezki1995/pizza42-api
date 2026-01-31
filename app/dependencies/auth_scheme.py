"""
JWT Authentication scheme dependency definition
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.security.jwt import VerifyJWT
from typing import Optional

# Security scheme shared across endpoints
auth_token_scheme = HTTPBearer()

def jwt_required(scopes: list[str], permissions: Optional[list[str]] = None , token: str = Depends(auth_token_scheme)) -> dict:
    """
    Args:
        scopes: list[str]
        permissions: Optional[list[str]] = None
        token (str, optional): _description_. Defaults to Depends(auth_token_scheme).
    Raises:
        HTTPException: when token validation returns ERROR

    Returns:
        dict: payload of the token
        
    To use the returned payload in the andpoint handling method add this payload parameter
    def get_orders(payload:dict = Depends[jwt_required]):
        ...
    """
    verifier = VerifyJWT(token=token.credentials, scopes=scopes, permissions=permissions)
    result = verifier.verify()
    if result.get("status") != "success":
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("payload", "Unauthorized"),
        )
    return result  # return payload for downstream use