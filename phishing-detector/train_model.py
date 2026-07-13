import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
import os

def train_phishing_detector():
    print("Step 1: Loading processed dataset...")
    if not os.path.exists('data/processed_dataset.csv'):
        print("Error: data/processed_dataset.csv not found. Please run prepare_data.py first.")
        return
        
    df = pd.read_csv('data/processed_dataset.csv')
    
    # Drop rows with missing values if any exist
    df = df.dropna()
    
    # Step 2: Separate features (X) and target label (y)
    # We drop 'label' from X because that's what we want to predict
    X = df.drop(columns=['label'])
    y = df['label']
    
    print(f"Dataset shape: {df.shape} (Rows, Columns)")
    print("\nFeatures being used for training:")
    print(list(X.columns))
    
    # Step 3: Split into Training (80%) and Testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nStep 4: Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Step 5: Evaluate the Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n================ MODEL EVALUATION ================")
    print(f"Accuracy Score: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("==================================================")
    
    # Step 6: Save the trained model to a file
    os.makedirs('models', exist_ok=True)
    model_path = 'models/phishing_model.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"\nSuccess! Model saved to '{model_path}'")

if __name__ == "__main__":
    train_phishing_detector()