# 🛡️ AI-Based Phishing Website Detection System

A full-stack web application that utilizes Machine Learning heuristics and live network verification to detect phishing URLs in real-time. 

---

## 🚀 Tech Stack

- **Frontend:** React (Vite), Lucide Icons
- **Backend:** Python, Flask, Flask-CORS
- **Machine Learning:** Scikit-Learn, Pandas, NumPy
- **Feature Extraction:** TLDExtract, Python-Whois

---

## ✨ Features

- **Lexical Analysis:** Evaluates URL structures (length, dot count, hyphens, presence of `@` or IP addresses).
- **Live SSL Verification:** Pings target servers to check for valid SSL certificates.
- **Machine Learning Classifier:** Employs a Random Forest model trained on live threat data to provide a dynamic phishing probability score.
- **Responsive Dashboard:** A clean, intuitive user interface for instant link verification.

---

## 🛠️ Installation & Setup

### 1. Backend Setup
Navigate to the root directory and activate your virtual environment:
```bash
# Activate Virtual Environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install pandas numpy scikit-learn tldextract python-whois Flask flask-cors

# Generate the dataset and train the model:

python prepare_data.py
python train_model.py

# Start the Flask server:

python app.py

# 2. Frontend Setup (React)
# Open a new, separate terminal window, navigate to the frontend folder, and launch the UI:

cd frontend
npm install
npm run dev

