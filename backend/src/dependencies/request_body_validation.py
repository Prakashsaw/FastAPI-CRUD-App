from fastapi import FastAPI, Request, HTTPException, status

async def validate_body(request: Request):
    """
    Validates the request body to ensure it is not empty.
    
    Note: Currently I am not using this dependency in any of the routes. But it can be used in the future if needed.
    """
    body = await request.json()
    if not body:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity!. Request body cannot be empty.",
        )
    