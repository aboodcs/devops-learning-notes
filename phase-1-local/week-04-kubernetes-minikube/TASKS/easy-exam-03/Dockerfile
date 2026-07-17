FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

RUN mkdir -p /app/uploads
ENV UPLOAD_DIR=/app/uploads
ENV PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]