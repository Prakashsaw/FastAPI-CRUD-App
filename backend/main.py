import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.user_route import user_router
from src.routes.book_route import book_router

app = FastAPI()

# CORS
origins = [
    "*",  # Allow all
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow all origins
    allow_credentials=True, # Allow cookies
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(book_router, prefix="/api/v1/book", tags=["Book"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to FastAPI CRUD Appication!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
