# Build Step #1
FROM node:16-alpine3.15 as build-step
RUN mkdir /app
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./frontend/package.json package.json
COPY ./frontend/src ./src
COPY ./frontend/public ./public
RUN npm install
RUN npm run build

# pull official base image
FROM python:3.10.7

# set work directory
WORKDIR /app

# install dependencies
COPY ./backend/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# copy project
COPY ./backend ./

EXPOSE 5000
WORKDIR /app
CMD ["gunicorn", "-b", ":5000", "app:app"]