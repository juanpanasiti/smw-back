# pip install -r requirements-dev.txt
docker compose up smw-db -d
fastapi dev src/entrypoints/api.py --host 0.0.0.0 --port 8000
