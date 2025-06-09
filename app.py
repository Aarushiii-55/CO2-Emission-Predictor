import os
from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("best_model.pkl")  # Updated to best_model.pkl as per your project

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        engine_size = request.form.get('engine_size', None)
        cylinders = request.form.get('cylinders', None)
        fuel_type = request.form.get('fuel_type', None)

        if not engine_size or not cylinders or not fuel_type:
            raise ValueError("All fields are required!")

        engine_size = float(engine_size)
        cylinders = int(cylinders)

        fuel_types = ['Petrol', 'Diesel', 'Hybrid']
        fuel_type_encoded = [1 if fuel_type == ft else 0 for ft in fuel_types]

        features = [engine_size, cylinders] + fuel_type_encoded
        feature_columns = ['engine_size', 'cylinders'] + [f'fuel_type_{ft}' for ft in fuel_types]
        features_df = pd.DataFrame([features], columns=feature_columns)

        prediction = model.predict(features_df)[0]
        prediction_text = f"Predicted CO2 Emission: {prediction:.2f} g/km"

        return render_template('index.html', prediction_text=prediction_text)
    
    except ValueError as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)