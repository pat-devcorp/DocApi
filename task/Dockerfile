###########
# BUILDER #
###########

# pull official base image
FROM python:3.11-slim as builder

# set work directory
WORKDIR /usr

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip

# install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.11-slim

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV APP_HOME=/home/services/task
RUN mkdir -p $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd 
COPY --from=builder /usr/wheels /wheels
COPY --from=builder /usr/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./src /home/services/task/src
COPY wsgi.py $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

WORKDIR /home/services/task

# run entrypoint.prod.sh
ENTRYPOINT ["/entrypoint.sh"]
