FROM python:3.8
WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev netcat-openbsd wget curl unzip bash

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY load-data.py .
COPY wait-for.sh .
COPY load-track-data.sh .
COPY entrypoint.sh .

RUN chmod +x wait-for.sh load-track-data.sh entrypoint.sh

# Install MinIO Client
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/bin/mc && \
    chmod +x /usr/bin/mc

CMD ["./entrypoint.sh"]
