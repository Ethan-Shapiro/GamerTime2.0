# Build Step #1
FROM node:16-alpine3.15 as build-step
RUN mkdir /frontend
WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json /frontend/package.json
COPY ./src ./src
COPY ./public ./public
RUN npm install
RUN npm run build

# Build step #2: nginx
FROM nginx:stable-alpine
COPY --from=build-step /frontend/build /usr/share/nginx/html
COPY nginx.default.conf /etc/nginx/conf.d/default.conf

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
ENV FLASK_ENV=production

# copy project
COPY . ./

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "app:app"]