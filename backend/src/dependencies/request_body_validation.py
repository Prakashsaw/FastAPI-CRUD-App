# Dependency to check for empty body
from fastapi import FastAPI, Request, HTTPException, status

async def validate_body(request: Request):
    # if in request itself body is empty then raise an exception
    body = await request.json()
    if not body:  # Check if the body is empty
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity!. Request body cannot be empty.",
        )
    
# Note: Currently I am not using this dependency in any of the routes. But it can be used in the future if needed.