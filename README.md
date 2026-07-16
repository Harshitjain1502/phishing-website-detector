# 🛡️ AI-Based Phishing Website Detection System

A full-stack web application that utilizes Machine Learning heuristics and live network verification to detect phishing URLs in real-time.

---

## 🚀 Tech Stack

* **Frontend:** React (Vite), Lucide Icons
* **Backend:** Python, Flask, Flask-CORS
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Feature Extraction:** TLDExtract, Python-Whois

---

## ✨ Features

* **Lexical Analysis:** Evaluates URL structures (length, dot count, hyphens, presence of `@` or IP addresses).
* **Live SSL Verification:** Pings target servers to check for valid SSL certificates.
* **Machine Learning Classifier:** Employs a Random Forest model trained on live threat data to provide a dynamic phishing probability score.
* **Responsive Dashboard:** A clean, intuitive user interface for instant link verification.

---

## 🛠️ Installation & Setup

Follow these steps to get the full-stack application running locally.

### 1. Backend Setup (Flask & ML)

Open a terminal window, navigate into the backend directory, and activate your virtual environment:

```bash
cd phishing-detector

# Activate Virtual Environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install pandas numpy scikit-learn tldextract python-whois Flask flask-cors

# Process the live PhishTank threat data and train your machine learning model:
python prepare_data.py
python train_model.py

# Start the local Flask API server:
python app.py

** ### 2. Frontend Setup (React) **

Open a new, separate terminal window, navigate to the frontend folder, and launch the user interface:

```bash
cd frontend

# Install packages
npm install

# Start the dev server
npm run dev
