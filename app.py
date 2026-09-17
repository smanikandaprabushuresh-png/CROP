import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "crop_recommendation_secret_key"

MODEL_PATH = "crop_model.pkl"

# Load the trained model
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    print(f"Warning: {MODEL_PATH} not found. Run train_model.py first.")

# Optional crop details dictionary for educational context on result page
CROP_DETAILS = {
    "Rice": "Rice is a staple kharif crop requiring high rainfall, warm temperatures, and nutrient-rich soil.",
    "Maize": "Maize thrives well in well-drained loamy soils with moderate temperature and rainfall.",
    "Chickpea": "Chickpea is a pulse crop that prefers cool weather and well-drained soils with good potassium.",
    "Kidneybeans": "Kidney beans require moderate temperature and good phosphorus levels.",
    "Pigeonpeas": "Pigeon peas are drought-tolerant legumes suitable for tropical and subtropical climates.",
    "Mothbeans": "Moth beans are hardy arid legumes that grow well in hot and low-rainfall zones.",
    "Mungbean": "Mung bean is a short-duration pulse crop that tolerates warm temperatures and moderate humidity.",
    "Blackgram": "Blackgram prefers warm, humid climates and loamy soil rich in organic matter.",
    "Lentil": "Lentil is a cool-season legume requiring moderate rainfall and well-aerated soil.",
    "Pomegranate": "Pomegranate prefers semi-arid climates with mild winters and warm dry summers.",
    "Banana": "Banana is a tropical fruit crop requiring rich fertile soil, high moisture, and warmth.",
    "Mango": "Mango grows well in warm tropical climates with well-defined dry seasons.",
    "Grapes": "Grapes flourish in warm, dry summers and mild winters with well-drained sandy loam soil.",
    "Watermelon": "Watermelon is a warm-season fruit requiring sandy loam soil, high warmth, and low rainfall.",
    "Muskmelon": "Muskmelon thrives in hot, dry climates with plenty of sunlight and warm sandy soils.",
    "Apple": "Apple is a temperate fruit crop requiring cool climate, high potassium, and moderate humidity.",
    "Orange": "Orange is a citrus fruit that flourishes in subtropical climates with well-drained soils.",
    "Papaya": "Papaya grows rapidly in tropical climates with rich, moist, and well-drained soil.",
    "Coconut": "Coconut is a coastal tropical plantation crop requiring high humidity and abundant rainfall.",
    "Cotton": "Cotton is an essential fiber cash crop that thrives in black cotton soil under warm conditions.",
    "Jute": "Jute is a natural fiber crop that requires hot, humid climates and heavy rainfall.",
    "Coffee": "Coffee thrives in cool to warm tropical highland climates with well-distributed rainfall."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")

@app.route("/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
        else:
            flash("Model file not found. Please train the model first.", "error")
            return redirect(url_for("recommendation"))

    try:
        # Extract inputs from form
        n = float(request.form.get("nitrogen", 0))
        p = float(request.form.get("phosphorus", 0))
        k = float(request.form.get("potassium", 0))
        temperature = float(request.form.get("temperature", 0))
        humidity = float(request.form.get("humidity", 0))
        ph = float(request.form.get("ph", 0))
        rainfall = float(request.form.get("rainfall", 0))

        input_data = pd.DataFrame([{
            'N': n,
            'P': p,
            'K': k,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }])
        
        # Predict crop
        prediction = model.predict(input_data)[0]
        crop_name = str(prediction).strip()
        crop_desc = CROP_DETAILS.get(crop_name, "This crop matches your provided soil and climate conditions.")

        entered_values = {
            "Nitrogen (N)": f"{n} kg/ha",
            "Phosphorus (P)": f"{p} kg/ha",
            "Potassium (K)": f"{k} kg/ha",
            "Temperature": f"{temperature} °C",
            "Humidity": f"{humidity} %",
            "Soil pH": f"{ph}",
            "Rainfall": f"{rainfall} mm"
        }

        return render_template(
            "result.html",
            crop=crop_name,
            description=crop_desc,
            entered_values=entered_values
        )

    except Exception as e:
        flash(f"Error making prediction: {str(e)}", "error")
        return redirect(url_for("recommendation"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
