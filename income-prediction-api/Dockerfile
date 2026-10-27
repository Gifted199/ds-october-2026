FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# MLflow configuration
ENV MLFLOW_TRACKING_URI=sqlite:////mlflow/mlflow.db

# Install Python dependencies
COPY requirements.txt .
RUN pip cache purge && pip install --no-cache-dir -r requirements.txt

# Copy API source and preprocessing pipeline
COPY app/ ./app/
COPY artifacts/ ./artifacts/
COPY streamlit_app.py .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]