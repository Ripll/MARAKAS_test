# pull official base image
FROM python:3.9.2-buster

RUN apt update
# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

# copy project
COPY . ./