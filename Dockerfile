# syntax=docker/dockerfile:1

FROM ozyviking/python-nginx:3.11 AS build-python

WORKDIR /home/www-data/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Using python poetry for the install.
COPY pyproject.toml /home/www-data/app/
COPY README.md /home/www-data/app/
RUN <<EOF
python -m pip install --upgrade pip
python -m pip install poetry
poetry config virtualenvs.in-project true
poetry install
EOF

# Using requirements.txt for the install. Use: `pip freeze --exclude-editable > requirements.freeze`           
# COPY requirements.freeze /home/www-data/app/
# RUN <<EOF
# python -m pip install --upgrade pip
# python -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.freeze
# EOF

###################
FROM ozyviking/python-nginx:3.11 AS final

LABEL org.opencontainers.image.authors="Zack Hankin <admin@hankin.io>"

WORKDIR /home/www-data/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

COPY --from=build-python --chown=www-data:www-data /home/www-data/app/.venv /home/www-data/app/.venv
COPY --chown=www-data:www-data UniService/ /home/www-data/app/
COPY --chown=www-data:www-data gunicorn/nginx.conf /etc/nginx/nginx.conf
COPY --chown=www-data:www-data gunicorn/gunicorn* /etc/gunicorn/
COPY --chown=www-data:www-data --chmod=777 scripts/ /docker-entrypoint.d/

ENV PATH=/docker-entrypoint.d:/home/www-data/app:/home/www-data/app/.venv/bin:${PATH}

RUN ln -s /etc/gunicorn/gunicorn.sh /etc/init.d/gunicorn

RUN <<EOF
mkdir /var/log/gunicorn
chown -R www-data:www-data /var/log/gunicorn
mv /home/www-data/app/build/static/* /var/www/static
chmod -R o-rwx /etc/gunicorn
EOF

RUN <<EOF
cat >> /root/.bashrc << EOFILE
alias start='service gunicorn start'
alias status='service gunicorn status'
alias stop='service gunicorn stop'
alias restart='service gunicorn restart'
EOF

HEALTHCHECK --retries=3 CMD service gunicorn status
SHELL ["bash", "-c"]
EXPOSE 80
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "nginx", "-g", "daemon off;" ]
