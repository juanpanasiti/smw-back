FROM python:3.13.1

WORKDIR /srv/project/

COPY ./requirements.txt /srv/project/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /srv/project/app
COPY ./logs /srv/project/logs
COPY ./.git /srv/project/.git
COPY ./run.sh /srv/project/run.sh
COPY ./alembic.ini /srv/project/alembic.ini
COPY ./migrations /srv/project/migrations

CMD ["sh", "run.sh"]