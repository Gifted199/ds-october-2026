import requests
import streamlit as st


# Configure the Streamlit page
st.set_page_config(
    page_title="Income Prediction",
    page_icon="📊",
    layout="centered",
)


# FastAPI prediction endpoint
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")


# Page heading
st.title("📊 Adult Census Income Prediction")
st.write(
    "Enter a customer's information below to predict "
    "their income category using our trained machine-learning model."
)


# Create the input form
with st.form("income_prediction_form"):

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=17,
            max_value=100,
            value=39,
            step=1,
        )

        workclass = st.selectbox(
            "Workclass",
            [
                "Private",
                "Self-emp-not-inc",
                "Self-emp-inc",
                "Federal-gov",
                "Local-gov",
                "State-gov",
                "Without-pay",
                "Never-worked",
            ],
        )

        education = st.selectbox(
            "Education",
            [
                "Bachelors",
                "HS-grad",
                "Some-college",
                "Masters",
                "Assoc-voc",
                "Assoc-acdm",
                "11th",
                "10th",
                "7th-8th",
                "9th",
                "12th",
                "5th-6th",
                "1st-4th",
                "Preschool",
                "Prof-school",
                "Doctorate",
            ],
        )

        education_num = st.number_input(
            "Education number",
            min_value=1,
            max_value=16,
            value=13,
            step=1,
        )

        marital_status = st.selectbox(
            "Marital status",
            [
                "Never-married",
                "Married-civ-spouse",
                "Divorced",
                "Separated",
                "Widowed",
                "Married-spouse-absent",
                "Married-AF-spouse",
            ],
        )

        occupation = st.selectbox(
            "Occupation",
            [
                "Adm-clerical",
                "Exec-managerial",
                "Handlers-cleaners",
                "Prof-specialty",
                "Other-service",
                "Sales",
                "Craft-repair",
                "Transport-moving",
                "Farming-fishing",
                "Machine-op-inspct",
                "Tech-support",
                "Protective-serv",
                "Armed-Forces",
                "Priv-house-serv",
            ],
        )

        relationship = st.selectbox(
            "Relationship",
            [
                "Not-in-family",
                "Husband",
                "Wife",
                "Own-child",
                "Unmarried",
                "Other-relative",
            ],
        )

    with col2:
        fnlwgt = st.number_input(
            "Final sampling weight",
            min_value=1,
            value=77516,
            step=1,
        )

        sex = st.selectbox(
            "Sex",
            ["Male", "Female"],
        )

        race = st.selectbox(
            "Race",
            [
                "White",
                "Black",
                "Asian-Pac-Islander",
                "Amer-Indian-Eskimo",
                "Other",
            ],
        )

        capital_gain = st.number_input(
            "Capital gain",
            min_value=0,
            value=0,
            step=100,
        )

        capital_loss = st.number_input(
            "Capital loss",
            min_value=0,
            value=0,
            step=100,
        )

        hours_per_week = st.number_input(
            "Hours worked per week",
            min_value=1,
            max_value=100,
            value=40,
            step=1,
        )

        native_country = st.selectbox(
            "Native country",
            [
                "United-States",
                "Mexico",
                "Philippines",
                "Germany",
                "Canada",
                "India",
                "England",
                "China",
                "Cuba",
                "Jamaica",
                "Other",
            ],
        )


    submit = st.form_submit_button(
        "Predict Income",
        use_container_width=True,
    )


# Send the customer's information to FastAPI
if submit:

    customer_data = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "education.num": education_num,
        "marital.status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital.gain": capital_gain,
        "capital.loss": capital_loss,
        "hours.per.week": hours_per_week,
        "native.country": native_country,
    }

    try:
        with st.spinner("Generating prediction..."):

            response = requests.post(
                API_URL,
                json=customer_data,
                timeout=60,
            )

        response.raise_for_status()
        result = response.json()

        st.subheader("Prediction Result")

        if result["predicted_class"] == 1:
            st.success("Predicted income: More than $50,000")
        else:
            st.info("Predicted income: $50,000 or less")

        st.metric(
            "Prediction score",
            f'{result["prediction_score"]:.2%}',
        )

        st.caption(
            "Classification threshold: "
            f'{result["classification_threshold"]}'
        )

        st.caption(
            "This is a model prediction, not a guarantee "
            "of a person's actual income."
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the prediction API. "
            "Check that your Docker container is running."
        )

    except requests.exceptions.Timeout:
        st.error(
            "The prediction request timed out. "
            "Please try again."
        )

    except requests.exceptions.RequestException as error:
        st.error(f"The prediction request failed: {error}")
