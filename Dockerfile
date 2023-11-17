FROM quay.io/astronomer/astro-runtime:9.5.0

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir psycopg2-binary==2.9.9 && \
    pip install --no-cache-dir Unidecode==1.3.7 && \
    deactivate
