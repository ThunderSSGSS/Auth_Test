FROM python:3.7-alpine

WORKDIR /code

COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps libpq gcc libffi-dev musl-dev postgresql-dev \
&& pip3 install --no-cache-dir --upgrade -r requirements.txt \
&& apk del .build-deps gcc libffi-dev musl-dev postgresql-dev libpq && apk add --no-cache libpq

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]