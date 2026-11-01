FROM python:3.13-slim

WORKDIR /app

# Upgrade pip and app packages globally
RUN python -m pip install --upgrade --no-cache-dir \
    pip \
    "setuptools>=78.1.1" \
    "urllib3>=2.8.0" \
    "msgpack>=1.2.3"

# Clean up stale Debian base system metadata files
RUN rm -rf /usr/lib/python3/dist-packages/setuptools* \
           /usr/lib/python3/dist-packages/urllib3* \
           /usr/lib/python3/dist-packages/msgpack*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]