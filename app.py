from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

# Minor update to trigger deploy

app = Flask(__name__)
CORS(app)

model_path = os.path.join(os.path.dirname(__file__), "salary_predict_model.ml")
model = joblib.load(model_path)


@app.route("/")
def home():
    """Landing page for the Salary Prediction API"""
    return (
        "<h1>Salary Prediction API</h1>"
        "<p>BAIS:3300 - Digital Product Development</p>"
        "<p>Luke Lockhart</p>"
    )


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict salary based on input JSON payload
    Expected keys: age, gender, country, highest_deg, coding_exp, title, company_size
    """
    print("inside predict")
    try:
        data = request.get_json()

        print(f"data from the user: {data}")

        required_fields = [
            "age",
            "gender",
            "country",
            "highest_deg",
            "coding_exp",
            "title",
            "company_size",
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing one or more required fields"}), 400

        # Ensure correct order and type
        features = [
            int(data["age"]),
            int(data["gender"]),
            int(data["country"]),
            int(data["highest_deg"]),
            int(data["coding_exp"]),
            int(data["title"]),
            int(data["company_size"]),
        ]

        print(f"features before using the model: {data}")

        prediction = model.predict([features])[0]

        print(f"prediction: {prediction}")

        return jsonify({"predicted_salary": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


import os

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
