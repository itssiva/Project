FROM nginx
RUN rm -r -f /etc/nginx/sites-enabled/default
RUN rm -r -f /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/
expose 80/tcp
RUN service nginx restart

