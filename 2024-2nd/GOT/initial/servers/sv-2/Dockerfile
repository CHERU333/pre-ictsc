FROM ubuntu:22.04

RUN apt-get update && apt-get install -y iproute2 iputils-ping apache2 apache2-utils

# Apacheの80ポートを81に変更
RUN a2dissite 000-default.conf && \
    sed -i 's/Listen 80/Listen 81/' /etc/apache2/ports.conf

# ページとBasic認証設定
RUN echo "Hello ICTSC!!!" > /var/www/html/ictsc.html && \
    htpasswd -b -c /etc/apache2/.htpasswd ictsc ictsc && \
    bash -c "printf '%s\n' \
'<VirtualHost *:81>' \
'  DocumentRoot /var/www/html' \
'  <Directory /var/www/html>' \
'    AuthType Basic' \
'    AuthName \"ictsc\"' \
'    AuthUserFile /etc/apache2/.htpasswd' \
'    Require valid-user' \
'  </Directory>' \
'</VirtualHost>' \
> /etc/apache2/sites-available/ictsc.conf"

RUN a2ensite ictsc.conf

CMD ["bash", "-lc", "sleep infinity"]
