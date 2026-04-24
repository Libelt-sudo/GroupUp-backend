from fastapi import HTTPException

EmailExistsException = HTTPException(status_code=409, detail="Email is already in use")

UsernameExistsException = HTTPException(status_code=409, detail="Username is already in use")