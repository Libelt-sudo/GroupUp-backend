from fastapi import HTTPException

authentication_exception = HTTPException(status_code=401, detail="Unauthorized. Failed to authenticate")