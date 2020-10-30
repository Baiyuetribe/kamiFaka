FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python db_init.py

EXPOSE 5000

# CMD [ "python", "./app.py" ]

ENTRYPOINT ["gunicorn", "-k", "gevent", "--bind", "0.0.0.0", "--workers", "8", "app:app"]