# pull official base image
FROM python:3.10.7

# set work directory
RUN mkdir /backend
WORKDIR /backend

# install dependencies
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# copy project
COPY . ./

EXPOSE 5000
CMD exec gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 8 --timeout 0 app:app