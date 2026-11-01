FROM python:3.13-slim

WORKDIR /app

# Step 1: Upgrade base system packages first
RUN python -m pip install --upgrade pip setuptools urllib3 msgpack

# Step 2: Copy requirements and install app dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Copy app code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]