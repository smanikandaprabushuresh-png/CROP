"""
train_model.py
Trains a Random Forest Classifier on the crop recommendation dataset
and saves the trained model to crop_model.pkl.
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_crop_model():
    dataset_path = os.path.join("dataset", "crop_data.csv")
    print(f"Loading dataset from: {dataset_path}")
    
    # 1. Load the dataset
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    print("Features:", list(df.columns[:-1]))
    print("Target:", df.columns[-1])
    
    # 2. Separate input features (X) and crop labels (y)
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # 3. Split into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Train a basic Random Forest classification model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Test Accuracy: {accuracy * 100:.2f}%")
    
    # 5. Save the trained model to crop_model.pkl
    model_output_path = "crop_model.pkl"
    with open(model_output_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved successfully to {model_output_path}")

if __name__ == "__main__":
    train_crop_model()
