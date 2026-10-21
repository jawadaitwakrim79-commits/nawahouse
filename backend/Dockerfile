FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# GeoLite2 lives in data/ and is not a Python package. Copy it on its own
# so the image contains GeoLite2-Country.mmdb whenever that file is in the
# build context (backend/data/ on the machine that runs docker build).
COPY data/ /app/data/

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
