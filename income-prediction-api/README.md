# Adult Census Income Prediction

## 1. Project Overview

This project uses a deep learning model to predict whether an individual's annual income is greater than $50,000 or $50,000 or less, based on demographic and employment-related information from the Adult Census Income dataset.

The project demonstrates how a trained machine learning model can be deployed through a REST API and accessed using a web application.

## 2. Business Problem

Understanding income patterns can help analysts explore relationships between demographic characteristics, employment, education, and income categories.

The objective is to develop a classification model that predicts an individual's income category from the available features.

This is an educational machine learning project. Predictions should not be treated as definitive assessments of an individual's financial circumstances.

## 3. Technologies Used

* Python
* TensorFlow and Keras
* Pandas
* Scikit-learn
* FastAPI
* Streamlit
* Docker
* Joblib

## 4. Application Architecture

The application consists of three main components:

1. **Streamlit frontend:** Collects customer information through a web form and displays the prediction.
2. **FastAPI backend:** Validates incoming data, applies the saved preprocessing pipeline, and returns the model prediction.
3. **Deep learning model:** Processes the transformed features and produces an income classification score.

Docker packages the API and its required model artifacts into a container.

## 5. Project Structure

```text
income-prediction-api/
├── app/
│   └── main.py
├── artifacts/
│   ├── preprocessor.joblib
│   └── income_classifier.keras
├── requirements.txt
├── Dockerfile
├── streamlit_app.py
└── README.md
```

## 6. Running the Application

### Prerequisites

* Docker Desktop
* A web browser

### Start the API container

If the container has already been created, start it using:

```powershell
docker start income-prediction-container
```

If it is already running, no additional command is necessary.

### Open the Streamlit application

From the project root directory, open a terminal and run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\income-prediction-api\streamlit_app.py
```

Open the local address displayed in the terminal, normally:

```text
http://localhost:8501
```

### Access the API documentation

With the Docker container running, open:

```text
http://localhost:8001/docs
```

This page provides interactive documentation for the FastAPI endpoints.

## 7. API Endpoints

| Method | Endpoint   | Purpose                                                |
| ------ | ---------- | ------------------------------------------------------ |
| GET    | `/`        | Checks whether the API is running.                     |
| POST   | `/predict` | Predicts an income category from customer information. |

## 8. Model Output

The prediction response includes:

* `predicted_income`: The predicted income category.
* `predicted_class`: The binary classification result.
* `prediction_score`: The model's output score.
* `classification_threshold`: The threshold used to assign the class.

The current classification threshold is 0.5.

## 9. Limitations and Responsible Use

* Predictions depend on the quality and representativeness of the training data.
* The prediction score should not automatically be interpreted as a calibrated probability.
* The model may reflect biases present in the source data.
* Predictions should not be used as the sole basis for consequential financial, employment, or eligibility decisions.
* Input data should be handled securely and in accordance with applicable privacy requirements.

## 10. Future Improvements

Potential improvements include:

* Automated testing of the API and user interface.
* Model monitoring and performance tracking.
* Input validation and clearer error messages.
* Secure deployment to a cloud platform.
* Evaluation of fairness and model performance across demographic groups.

## 11. Project Status

The model has been integrated with a FastAPI backend, packaged into a Docker container, and connected to a Streamlit user interface. A local prediction test has completed successfully.
