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