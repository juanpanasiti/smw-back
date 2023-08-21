FROM python:3.11

WORKDIR /srv/project/

COPY ./requirements.txt /srv/project/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /srv/project/app
COPY ./logs /srv/project/logs

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]