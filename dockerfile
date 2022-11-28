FROM python:3.8-slim-buster
WORKDIR /app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]

ENV PORT 5000
EXPOSE 5000
CMD [ "main.py" ]