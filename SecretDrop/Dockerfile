FROM python:3.13-slim

WORKDIR /app

# Uninstall default system wheels and force-reinstall clean versions
RUN python -m pip install --upgrade --force-reinstall --no-cache-dir \
    pip \
    "setuptools>=78.1.1" \
    "urllib3>=2.8.0" \
    "msgpack>=1.2.3"

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]