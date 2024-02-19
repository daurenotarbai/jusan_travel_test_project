from fastapi import HTTPException

class HTTPUnauthenticatedException(HTTPException):
    """Raises on unauthenticated access."""
    ...


class HTTPUnauthorizedException(HTTPException):
    """Raises on unauthorized access."""
    ...