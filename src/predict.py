import os
import joblib
import pandas as pd

# Correct path to model and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "artifacts", "loan_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "artifacts", "scaler.pkl"))


def predict_loan(Gender, Married, Dependents, Education,
                 Self_Employed, ApplicantIncome, CoapplicantIncome,
                LoanAmount, Loan_Amount_Term, Credit_History, Property_Area):
    

    # Convert user inputs into same encoded format used during training
    gender_map = {"Male": 1, "Female": 0}
    married_map = {"Yes": 1, "No": 0}
    education_map = {"Graduate": 0, "Not Graduate": 1}
    self_emp_map = {"No": 0, "Yes": 1}
    property_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    dependents_map = {"0": 0, "1": 1, "2": 2, "3+": 3}

    # Making the data frame for prediction
    input_data = pd.DataFrame([{
        "Gender": gender_map[Gender],
        "Married": married_map[Married],
        "Dependents": dependents_map[Dependents],
        "Education": education_map[Education],
        "Self_Employed": self_emp_map[Self_Employed],
        "ApplicantIncome": ApplicantIncome,
        "CoapplicantIncome": CoapplicantIncome,
        "LoanAmount": LoanAmount,
        "Loan_Amount_Term": Loan_Amount_Term,
        "Credit_History": Credit_History,
        "Property_Area": property_map[Property_Area]
    }])

    input_data = input_data[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                     'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                     'Loan_Amount_Term', 'Credit_History', 'Property_Area']]

    # Scale input because Logistic Regression was trained on scaled data
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # Probability
    probability = model.predict_proba(input_scaled)[0][1]   # probability of class 1 = Approved

    if prediction == 1:
        status = "Approved"
    else:
        status = "Rejected"

    return status, probability