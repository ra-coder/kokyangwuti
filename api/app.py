import uvicorn
from fastapi import FastAPI

from src.api import router as api_router

app = FastAPI(root_path="/api")
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    # uvicorn app:app --reload
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
    )
