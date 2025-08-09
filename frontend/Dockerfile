# frontend/Dockerfile

# 1) Build do React/Vite (ajuste conforme seu front)
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend /app
RUN npm run build

# 2) Nginx para servir estático + proxy /api -> api:8000
FROM nginx:alpine
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
