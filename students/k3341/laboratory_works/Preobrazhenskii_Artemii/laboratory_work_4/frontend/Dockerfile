# --- Stage 1: Build Frontend ---
FROM node:22-alpine AS builder

WORKDIR /app

# Копируем package-файлы для кэширования layer
COPY frontend/package*.json ./ 

RUN npm install

COPY frontend/. ./frontend

# Allow injecting the API base URL at build time so Vite bakes it into the bundle.
# Usage: `docker build --build-arg VITE_API_BASE_URL=http://app:8082/api -f frontend/Dockerfile .`
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Собираем проект Vite в dist/
RUN npm run --prefix frontend build

# --- Stage 2: Serve with Nginx ---
FROM nginx:alpine AS runner

# Копируем билд в Nginx
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

COPY nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]