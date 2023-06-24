FROM python:3.11-alpine
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt
COPY src/ /app
WORKDIR /app
EXPOSE 5001
COPY src1/ /app
CMD ["python3", "main.py"]
