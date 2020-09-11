FROM python:3-alpine

ENV DJANGO_SETTINGS_MODULE=ffplayout.settings.production

# get ffplayout-api and all dependencies
RUN apk update && \
    apk add build-base gcc linux-headers libffi-dev zeromq-dev && \
    cd /opt && \
    wget "https://github.com/ffplayout/ffplayout-api/archive/master.zip" && \
    unzip 'master.zip' && \
    mv 'ffplayout-api-master' 'ffplayout-api' && \
    rm master.zip && \
    cd ffplayout-api && \
    pip install --no-cache-dir -r requirements-base.txt && \
    mkdir /etc/ffplayout && \
    # cleanup
    apk del build-base gcc linux-headers

RUN cd /opt/ffplayout-api/ffplayout && \
    sed -i "s/---a-very-important-secret-key\:-generate-it-new---/$(python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())')/g" ffplayout/settings/production.py && \
    sed -i "s/USE_SOCKET = False/USE_SOCKET = True/g" ffplayout/settings/common.py && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic && \
    python manage.py loaddata ../docs/db_data.json && \
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

WORKDIR /opt/ffplayout-api/ffplayout
EXPOSE 8001

CMD ["/usr/local/bin/gunicorn", "--workers", "4", "--worker-class=gevent", "--timeout", "10800", "--log-level=info", "--log-file=-", "--access-logfile=-", "--bind", "127.0.0.1:8001", "ffplayout.wsgi:application"]
