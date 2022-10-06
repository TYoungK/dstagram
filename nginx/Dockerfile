FROM nginx:1.18.0-alpine
ENV PYTHONUNBUFFERED 1
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d