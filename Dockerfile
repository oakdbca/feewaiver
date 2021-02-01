# Prepare the base environment.
FROM ubuntu:20.04 as builder_base_feewaiver
MAINTAINER asi@dbca.wa.gov.au
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
ENV PRODUCTION_EMAIL=False
ENV EMAIL_INSTANCE="DEV"
ENV NON_PROD_EMAIL="brendan.blackford@dbca.wa.gov.au,walter.genuit@dbca.wa.gov.au,aaron.farr@dbca.wa.gov.au"
ENV SECRET_KEY="ThisisNotRealKey"
ARG build_tag=0.0.0
ENV BUILD_TAG=$build_tag
RUN echo "*************************************************** Build TAG = $build_tag ***************************************************"
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends -y wget git libmagic-dev gcc binutils libproj-dev gdal-bin python3 python3-setuptools python3-dev python3-pip tzdata cron rsyslog gunicorn libreoffice
RUN apt-get install --no-install-recommends -y libpq-dev patch
RUN apt-get install --no-install-recommends -y postgresql-client mtr htop vim ssh
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip
# Install Python libs from requirements.txt.
FROM builder_base_feewaiver as python_libs_feewaiver
WORKDIR /app
COPY requirements.txt ./
RUN touch /app/git_hash
RUN pip install --no-cache-dir -r requirements.txt \
  # Update the Django <1.11 bug in django/contrib/gis/geos/libgeos.py
  # Reference: https://stackoverflow.com/questions/18643998/geodjango-geosexception-error
  #&& sed -i -e "s/ver = geos_version().decode()/ver = geos_version().decode().split(' ')[0]/" /usr/local/lib/python3.6/dist-packages/django/contrib/gis/geos/libgeos.py \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*

COPY libgeos.py.patch /app/
RUN patch /usr/local/lib/python3.8/dist-packages/django/contrib/gis/geos/libgeos.py /app/libgeos.py.patch
RUN rm /app/libgeos.py.patch

# Install the project (ensure that frontend projects have been built prior to this step).
FROM python_libs_feewaiver

COPY gunicorn.ini manage_fw.py ./
#COPY ledger ./ledger
COPY timezone /etc/timezone
ENV TZ=Australia/Perth
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN touch /app/.env
COPY .git ./.git
COPY feewaiver ./feewaiver
RUN python manage_fw.py collectstatic --noinput

RUN mkdir /app/tmp/
RUN chmod 777 /app/tmp/

#COPY cron /etc/cron.d/dockercron
COPY startup.sh /
## Cron start
#RUN service rsyslog start
#RUN chmod 0644 /etc/cron.d/dockercron
#RUN crontab /etc/cron.d/dockercron
#RUN touch /var/log/cron.log
#RUN service cron start
RUN chmod 755 /startup.sh
# cron end
EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
