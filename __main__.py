import uvicorn

from app.core import settings


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=settings.PORT, reload=True)
