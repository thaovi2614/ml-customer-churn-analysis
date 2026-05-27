from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# load model
model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # tạo vector mặc định = 0
    input_dict = {f: 0 for f in features}

    # ===== 1. numeric =====
    numeric_fields = [
        "Number of Referrals",
        "Tenure in Months",
        "Monthly Charge",
        "Age",
        "Number of Dependents",
        "Total Revenue",
        "Total Long Distance Charges",
        "Total Refunds",
        "Total Charges"
    ]

    for field in numeric_fields:
        if field in input_dict:
            input_dict[field] = float(data.get(field, 0))

    # ===== 2. categorical =====

    # Contract
    contract = data.get("Contract", "")
    if f"Contract_{contract}" in input_dict:
        input_dict[f"Contract_{contract}"] = 1

    # Payment Method
    pm = data.get("Payment Method", "")
    if f"Payment Method_{pm}" in input_dict:
        input_dict[f"Payment Method_{pm}"] = 1

    # City
    city = data.get("City", "")
    if f"City_{city}" in input_dict:
        input_dict[f"City_{city}"] = 1

    # Yes / No
    yes_fields = [
        "Internet Service",
        "Streaming Movies",
        "Online Security",
        "Streaming Music",
        "Premium Tech Support"
    ]

    for field in yes_fields:
        if data.get(field) == "Yes":
            key = f"{field}_Yes"
            if key in input_dict:
                input_dict[key] = 1

    # ===== 3. tạo input =====
    input_data = [input_dict[f] for f in features]
    input_array = np.array(input_data).reshape(1, -1)
    

    prediction = model.predict(input_array)[0]
    proba = model.predict_proba(input_array)[0][1]


    return jsonify({
        "prediction": int(prediction),
        "probability": float(proba)
    })

print("File is running...")

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)
    
# python app.py