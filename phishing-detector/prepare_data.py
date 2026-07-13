import pandas as pd
import numpy as np
from extractor import extract_features
import time

def load_and_prepare_data():
    print("Step 1: Fetching live phishing URLs from PhishTank...")
    # PhishTank provides a live updated CSV of verified active phishing targets
    phishtank_url = "http://data.phishtank.com/data/online-valid.csv"
    
    try:
        phish_df = pd.read_csv(phishtank_url)
        # We only need the URL column
        phish_urls = phish_df['url'].tolist()
        print(f"Successfully loaded {len(phish_urls)} active phishing URLs.")
    except Exception as e:
        print(f"Error downloading PhishTank data: {e}")
        print("Fallback: Please download the CSV manually from PhishTank and place it in data/online-valid.csv")
        return

    print("\nStep 2: Generating legitimate URLs...")
    # For a balanced dataset, we need safe URLs. 
    # In production, you'd load a massive list (like Majestic Million). 
    # Here is a robust baseline list of top safe domains to start with:
    safe_domains = [
        "https://www.google.com", "https://www.youtube.com", "https://www.facebook.com",
        "https://www.wikipedia.org", "https://www.amazon.com", "https://www.apple.com",
        "https://www.microsoft.com", "https://www.netflix.com", "https://www.linkedin.com",
        "https://www.instagram.com", "https://www.twitter.com", "https://www.reddit.com"
    ]
    
    # We will sample a subset of phishing URLs to keep our initial training fast and balanced
    sample_size = min(1000, len(phish_urls)) 
    phish_sample = np.random.choice(phish_urls, sample_size, replace=False)
    
    # Expand our safe domains list to match the sample size for a balanced dataset (50/50 split)
    # In a full run, you would load a Kaggle benign URL dataset file here instead.
    safe_sample = np.random.choice(safe_domains, sample_size, replace=True)

    print("TLDEXTRACT/Features processing started...")
    
    processed_data = []
    
    # Process Phishing URLs (Label = 1)
    print("Processing Phishing URLs...")
    for url in phish_sample:
        features = extract_features(url)
        if features:
            features['label'] = 1
            processed_data.append(features)
            
    # Process Safe URLs (Label = 0)
    print("Processing Safe URLs...")
    for url in safe_sample:
        features = extract_features(url)
        if features:
            features['label'] = 0
            processed_data.append(features)

    # Convert to Dataframe and save
    dataset_df = pd.DataFrame(processed_data)
    dataset_df.to_csv("data/processed_dataset.csv", index=False)
    print(f"\nSuccess! Saved {len(dataset_df)} processed rows to 'data/processed_dataset.csv'")

if __name__ == "__main__":
    # Ensure the data folder exists
    import os
    os.makedirs('data', exist_ok=True)
    
    load_and_prepare_data()