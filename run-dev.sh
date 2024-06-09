pip install -r requirements-dev.txt
docker compose up smw-db -d
#uvicorn "app.app:app" --host 0.0.0.0 --port 8000 --reload
