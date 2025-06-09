import os
from flask import Flask, request, render_template

app = Flask(__name__)

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

        # Convert to proper types carefully
        engine_size = float(engine_size)
        cylinders = int(cylinders)

        # Your prediction code here...

        prediction_text = f"Predicted CO2 Emission: {engine_size * cylinders * 10} g/km"

        return render_template('index.html', prediction_text=prediction_text)
    
    except ValueError as e:
        # Pass error message to front-end
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
