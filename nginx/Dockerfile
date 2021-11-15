FROM nginx:stable


RUN  apt-get update \
      && apt-get install -y cron certbot python-certbot-nginx bash wget


VOLUME /etc/letsencrypt

CMD [ "sh", "-c", "cron && nginx -g 'daemon off;'" ]