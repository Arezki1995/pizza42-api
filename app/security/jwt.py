from app.configuration.config import load_config
from typing import Any, Dict, Optional
import jwt


class VerifyJWT:
    """
    Verifies a JWT token using PyJWT and a JWKS endpoint, with optional scope and
    permission checks.

    Standardized return structure:
    {
        "status": "success" | "error",
        "type": <error type or None if success>,
        "payload": <payload dict if success or error message if error>
    }
    """

    def __init__(
        self,
        token: str,
        permissions: Optional[list[str]] = None,
        scopes: Optional[str] = None,
    ) -> None:
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config: Dict[str, Any] = load_config()
        self.signing_key = None
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self) -> Dict[str, Any]:
        """
        Verify the token's signature and claims. Optionally verify scopes and permissions.

        Returns:
            Standardized response object.
        """
        # Step 1: Retrieve signing key
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "type": "PyJWKClientError", "payload": str(error)}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "type": "DecodeError", "payload": str(error)}

        # Step 2: Decode/verify the token
        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except jwt.PyJWTError as error:
            return {"status": "error", "type": "JWTDecodeError", "payload": str(error)}
        except Exception as error:
            return {"status": "error", "type": "UnknownError", "payload": str(error)}

        # Step 3: Optional scope verification
        if self.scopes:
            result = self._check_claims(
                payload=payload,
                claim_name="scope",
                claim_type=str,
                expected_value=self.scopes.split(" "),
            )
            if result.get("status") == "error":
                return result

        # Step 4: Optional permissions verification
        if self.permissions:
            result = self._check_claims(
                payload=payload,
                claim_name="permissions",
                claim_type=list,
                expected_value=self.permissions,
            )
            if result.get("status") == "error":
                return result

        # Step 5: All checks passed
        return {"status": "success", "type": None, "payload": payload}

    def _check_claims(
        self,
        payload: Dict[str, Any],
        claim_name: str,
        claim_type: type,
        expected_value: Any,
    ) -> Dict[str, Any]:
        """
        Validate a claim exists, has the correct type, and contains all expected values.

        Returns:
            Standardized response dict.
        """
        if claim_name not in payload or not isinstance(payload[claim_name], claim_type):
            return {
                "status": "error",
                "type": "MissingOrInvalidClaim",
                "payload": f"No claim '{claim_name}' found in token or invalid type.",
            }

        payload_claim = payload[claim_name]
        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for value in expected_value:
            if value not in payload_claim:
                return {
                    "status": "error",
                    "type": "InsufficientClaim",
                    "payload": (
                        f"Insufficient {claim_name} ({value}). You don't have access to this resource"
                    ),
                }

        return {"status": "success", "type": None, "payload": None}

    def __repr__(self) -> str:
        return (
            f"OAuth CONFIG - DOMAIN: {self.config['DOMAIN']}, ISSUER: {self.config['ISSUER']}"
        )