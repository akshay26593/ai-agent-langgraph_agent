# ---- Base Image ----
FROM python:3.11-slim

# ---- Set Working Directory ----
WORKDIR /app

# ---- Copy Code ----
COPY . /app

# ---- Install Dependencies ----
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# ---- Expose Port ----
EXPOSE 8080

# ---- Run FastAPI ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
