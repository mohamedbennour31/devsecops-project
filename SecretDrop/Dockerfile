FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade pip, setuptools, wheel, urllib3, and msgpack to clean vulnerable default packages
RUN pip install --upgrade pip setuptools wheel urllib3 msgpack && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]