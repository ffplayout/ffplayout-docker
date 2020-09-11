FROM node:lts-alpine AS build-stage

ENV NUXT_TELEMETRY_DISABLED=1

# get ffplayout-api and all dependencies
RUN cd /opt && \
    wget "https://github.com/ffplayout/ffplayout-frontend/archive/master.zip" && \
    unzip 'master.zip' && \
    mv 'ffplayout-frontend-master' 'ffplayout-frontend' && \
    rm master.zip && \
    cd ffplayout-frontend && \
    echo "BASE_URL='http://localhost:8088'" > .env && \
    echo "API_URL='http://localhost:8001'" >> .env && \
    npm install && \
    npm run build && \
    rm -rf node_modules

FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /opt/ffplayout-frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
