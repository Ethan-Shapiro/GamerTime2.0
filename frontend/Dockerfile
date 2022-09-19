# base image
FROM node:16-alpine3.15

RUN mkdir /frontend
WORKDIR /frontend
COPY package.json /frontend/package.json
RUN npm install

# start app
CMD ["npm", "start"]

EXPOSE 3000