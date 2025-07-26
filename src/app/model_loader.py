import joblib

model = joblib.load("model/model.pkl")

feature_columns = [
    "amount", "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest"
]
