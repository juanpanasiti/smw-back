import uvicorn

from src.config import settings


if __name__ == '__main__':
    uvicorn.run('src.entrypoints.api:app', host='0.0.0.0', port=settings.PORT, reload=True)
