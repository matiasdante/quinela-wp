# syntax=docker/dockerfile:1
FROM nginx:1.27-alpine

# Copy full nginx config (este archivo incluye http/events/server)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static frontend
COPY frontend/ /var/www/quinela-frontend/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -q -O - http://localhost/ | grep -q '<title>' || exit 1
