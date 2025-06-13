from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model, scaler, and feature columns
model = joblib.load('best__model.pkl')
scaler = joblib.load('Scalerss.pkl')
encoded_columns = joblib.load('Featuress.pkl')

# ✅ Define categorical columns used during training
categorical_cols = ["Vehicle_Class", "Transmission", "Fuel_Type"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user inputs
        Engine_Size = request.form.get('Engine_Size')
        Cylinders = request.form.get('Cylinders')
        Fuel_Consumption_Comb = request.form.get('Fuel_Consumption_Comb')
        Fuel_Type = request.form.get('Fuel_Type')
        Vehicle_Class = request.form.get('Vehicle_Class')
        Transmission = request.form.get('Transmission')

        # Validate inputs
        if not all([Engine_Size, Cylinders, Fuel_Consumption_Comb, Fuel_Type, Vehicle_Class, Transmission]):
            return render_template('index.html', prediction_text="Error: All fields are required.")

        # Convert inputs to proper types
        Engine_Size = float(Engine_Size)
        Cylinders = int(Cylinders)
        Fuel_Consumption_Comb = float(Fuel_Consumption_Comb)

        # Standardize Fuel_Type input
        fuel_type_mapping = {
            'premium gasoline': 'Premium Gasoline',
            'regular gasoline': 'Regular Gasoline',
            'ethanol(e85)': 'Ethanol(E85)',
            'diesel': 'Diesel'
        }
        Fuel_Type = fuel_type_mapping.get(Fuel_Type.strip().lower(), Fuel_Type)

        # Assemble input
        input_data = {
            'Engine_Size': Engine_Size,
            'Cylinders': Cylinders,
            'Fuel_Consumption_Comb': Fuel_Consumption_Comb,
            'Fuel_Consumption_City': 10.0,
            'Fuel_Consumption_Hwy': 7.0,
            'Vehicle_Class': Vehicle_Class,
            'Transmission': Transmission,
            'Fuel_Type': Fuel_Type
        }

        input_df = pd.DataFrame([input_data])

        # One-hot encode and align with training columns
        input_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)
        input_aligned = pd.DataFrame(0, index=[0], columns=encoded_columns)

        for col in input_encoded.columns:
            if col in encoded_columns:
                input_aligned[col] = input_encoded[col].iloc[0]

        # Scale and predict
        input_scaled = scaler.transform(input_aligned)
        prediction = model.predict(input_scaled)

        return render_template('index.html', prediction_text=f"Predicted CO₂ Emission: {prediction[0]:.2f} g/km")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
