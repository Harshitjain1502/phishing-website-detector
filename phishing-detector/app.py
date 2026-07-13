from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
from extractor import extract_features

app = Flask(__name__)
CORS(app)  # Enables React to communicate with this API safely

# Load the trained ML model globally on startup
MODEL_PATH = 'models/phishing_model.pkl'
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("🤖 Machine Learning model loaded successfully!")
else:
    print("⚠️ Warning: Trained model file not found! Please run train_model.py first.")

@app.route('/api/predict', methods=['POST'])
def predict_phishing():
    if model is None:
        return jsonify({"error": "ML model is not available on the server."}), 500

    # Get data from React request
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data['url']

    # 1. Extract features using our Phase 1 script
    features_dict = extract_features(url)
    if not features_dict:
        return jsonify({"error": "Invalid URL structure or formatting"}), 400

    # 2. Convert features dictionary to a 2D array matching model training structure
    # The order of features MUST perfectly match the column names used during training
    feature_features_list = [
        features_dict['url_length'],
        features_dict['domain_length'],
        features_dict['qty_dots'],
        features_dict['qty_hyphen'],
        features_dict['qty_at'],
        features_dict['qty_question'],
        features_dict['qty_equal'],
        features_dict['is_ip'],
        features_dict['has_subdomain'],
        features_dict['has_valid_ssl']
    ]
    
    input_data = np.array([feature_features_list])

    # 3. Generate Prediction
    # predict_proba returns [probability_of_safe, probability_of_phishing]
    probabilities = model.predict_proba(input_data)[0]
    phishing_probability = float(probabilities[1]) # Probability of being class 1 (phishing)
    prediction = int(model.predict(input_data)[0])

    # 4. Construct JSON Response
    response = {
        "url": url,
        "is_phishing": prediction,
        "probability": round(phishing_probability * 100, 2), # Convert to percentage
        "details": features_dict
    }

    return jsonify(response)

if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(debug=True, port=5000)