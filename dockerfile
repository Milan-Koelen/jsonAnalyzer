FROM python:3.8-slim-buster
WORKDIR /app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
ENV PORT 5000
EXPOSE 5000
ENTRYPOINT FLASK_APP= /app.py flask run --host=0.0.0.0


