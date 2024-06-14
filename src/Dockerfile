# uvicorn-gunicorn-docker Copyright (c) 2019 Sebastián Ramírez
# Modified version of https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/python3.11.dockerfile

FROM python:3.12

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

RUN chmod +x /app/start.sh
RUN chmod +x /app/start-reload.sh

WORKDIR /app/

ENV PYTHONPATH=/app
ENV MODULE_NAME="project.asgi"
ENV VARIABLE_NAME="application"
ENV PROJECT_ENVIRONMENT="prod"
ENV PROJECT_ADMIN_PATH="admin/"

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start.sh"]