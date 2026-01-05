# ---- Base Image ----
FROM python:3.11-slim

# ---- Set Working Directory ----
WORKDIR /app

# ---- Copy Code ----
COPY . /app

# ---- Install Dependencies ----
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# ---- Create writable data directory ----
RUN mkdir -p /app/data/pdfs && chmod -R 777 /app/data

# ---- Expose Port ----
EXPOSE 8080

# ---- Run FastAPI ----
# Add max request size to handle PDF uploads
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--limit-max-request-size", "200"]
