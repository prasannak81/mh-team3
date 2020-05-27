FROM node:12-alpine AS base

WORKDIR /usr/local/src

COPY tsconfig.json .
COPY package.json .
COPY package-lock.json .

RUN npm install

COPY public/ public/
COPY src/ src/

FROM base AS test

ENV CI=true

RUN npm run test

FROM base AS build

RUN npm run build

FROM nginx AS final

COPY nginx.conf /etc/nginx/conf.d/default.tmpl

ARG API_SERVICE=api:8080
ENV API_SERVICE=$API_SERVICE

RUN envsubst < /etc/nginx/conf.d/default.tmpl > /etc/nginx/conf.d/default.conf

COPY --from=build /usr/local/src/build /usr/share/nginx/html
