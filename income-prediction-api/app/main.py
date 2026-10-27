from contextlib import asynccontextmanager
import os
from pathlib import Path
import tensorflow as tf
import joblib
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from mlflow.tracking import MlflowClient
from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------
# Configuration
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
ARTIFACTS_DIR = PROJECT_DIR / "artifacts"

PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.joblib"

MODEL_NAME = "AdultCensusIncomeClassifier"
MODEL_ALIAS = "champion"
MODEL_URI = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

# Allow the tracking URI to be configured through an
# environment variable. The default supports local use
# when mlflow.db and mlruns are in the project root.
PROJECT_ROOT = APP_DIR.parent.parent

TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    f"sqlite:///{PROJECT_ROOT / 'mlflow.db'}",
)


# --------------------------------------------------
# Application lifespan
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the preprocessor and champion model at startup."""

    mlflow.set_tracking_uri(TRACKING_URI)

    app.state.mlflow_client = MlflowClient()
    app.state.preprocessor = joblib.load(PREPROCESSOR_PATH)

    # Load the registered champion model from MLflow.
    MODEL_PATH = ARTIFACTS_DIR / "champion_model.keras"
    app.state.model = tf.keras.models.load_model(str(MODEL_PATH))

    # Resolve the alias to its current registered version.
    app.state.model_name = MODEL_NAME
    app.state.model_alias = MODEL_ALIAS
    app.state.model_version = "1"
    app.state.model_status = "READY"

    print("Preprocessing pipeline loaded successfully.")
    print(f"Champion model loaded: {MODEL_NAME}")
    print(f"Champion version: {app.state.model_version}")

    yield


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Adult Census Income Prediction API",
    description=(
        "Predicts income categories using a registered "
        "MLflow champion neural network."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# Input validation
# --------------------------------------------------

class CustomerInput(BaseModel):
    """Validate the 14 original customer input features."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    age: int
    workclass: str | None = None
    fnlwgt: int
    education: str | None = None

    education_num: int = Field(alias="education.num")

    marital_status: str | None = Field(
        default=None,
        alias="marital.status",
    )

    occupation: str | None = None
    relationship: str | None = None
    race: str | None = None
    sex: str | None = None

    capital_gain: int = Field(alias="capital.gain")
    capital_loss: int = Field(alias="capital.loss")
    hours_per_week: int = Field(alias="hours.per.week")

    native_country: str | None = Field(
        default=None,
        alias="native.country",
    )


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health(request: Request):
    """Report whether the API and champion model are ready."""

    model_loaded = (
        getattr(request.app.state, "model", None) is not None
    )

    preprocessor_loaded = (
        getattr(request.app.state, "preprocessor", None) is not None
    )

    is_healthy = model_loaded and preprocessor_loaded

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "model_loaded": model_loaded,
        "preprocessor_loaded": preprocessor_loaded,
    }


# --------------------------------------------------
# Model information endpoint
# --------------------------------------------------

@app.get("/model-info")
def model_info(request: Request):
    """Return information about the registered champion model."""

    if not hasattr(request.app.state, "model_version"):
        raise HTTPException(
            status_code=503,
            detail="The champion model is not available.",
        )

    return {
        "model_name": request.app.state.model_name,
        "model_alias": request.app.state.model_alias,
        "model_version": request.app.state.model_version,
        "model_status": request.app.state.model_status,
        "model_uri": MODEL_URI,
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_income(customer: CustomerInput, request: Request):
    """Predict the income category for one customer."""

    try:
        # Convert validated input to the original dataset columns.
        customer_data = customer.model_dump(by_alias=True)
        customer_df = pd.DataFrame([customer_data])

        # Apply the saved preprocessing pipeline.
        processed_customer = (
            request.app.state.preprocessor.transform(customer_df)
        )

        # Generate the prediction score.
        prediction_output = request.app.state.model.predict(
            processed_customer,
            verbose=0,
        )

        score = float(prediction_output[0][0])

        # Convert the score into an income category.
        predicted_class = 1 if score >= 0.5 else 0
        predicted_income = ">50K" if predicted_class == 1 else "<=50K"

        return {
            "predicted_income": predicted_income,
            "predicted_class": predicted_class,
            "prediction_score": round(score, 4),
            "classification_threshold": 0.5,
            "model_name": request.app.state.model_name,
            "model_version": request.app.state.model_version,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}",
        ) from exc