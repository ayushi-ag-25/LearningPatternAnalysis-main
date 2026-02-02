import pandas as pd
import joblib
import os

# Initialize global variables for the model and scaler
_model = None
_scaler = None

def load_regression_assets():
    global _model, _scaler
    
    # Use relative paths from the project root
    MODEL_PATH = "models/regression_model.pkl"
    SCALER_PATH = "models/regression_scaler.pkl"
    
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            # Fallback for when running from within the utilities folder
            MODEL_PATH = "../models/regression_model.pkl"
            _model = joblib.load(MODEL_PATH)
            
    if _scaler is None:
        if os.path.exists(SCALER_PATH):
            _scaler = joblib.load(SCALER_PATH)
        else:
            # Fallback for when running from within the utilities folder
            SCALER_PATH = "../models/regression_scaler.pkl"
            _scaler = joblib.load(SCALER_PATH)
            
    return _model, _scaler

def predict_exam_score(data):
    """
    Independent logic for Mayank's model.
    Accepts dict or DataFrame, returns float or list of floats.
    """
    model, scaler = load_regression_assets()
    
    # Convert dict to DataFrame if necessary
    df = pd.DataFrame([data]) if isinstance(data, dict) else data.copy()
    
    # Comprehensive mapping for ALL categorical columns required by the model
    mapping = {
        'Motivation_Level': {'Low': 0, 'Medium': 1, 'High': 2},
        'Internet_Access': {'No': 0, 'Yes': 1},
        'Learning_Disabilities': {'No': 0, 'Yes': 1},
        'School_Type': {'Public': 0, 'Private': 1},
        'Peer_Influence': {'Negative': 0, 'Neutral': 1, 'Positive': 2},
        'Parental_Education_Level': {'High School': 0, 'College': 1, 'Postgraduate': 2},
        'Distance_from_Home': {'Near': 0, 'Moderate': 1, 'Far': 2},
        'Gender': {'Female': 0, 'Male': 1},
        'Extracurricular_Activities': {'No': 0, 'Yes': 1},
        'Access_to_Resources': {'Low': 0, 'Medium': 1, 'High': 2},
        'Parental_Involvement': {'Low': 0, 'Medium': 1, 'High': 2},
        'Teacher_Quality': {'Low': 0, 'Medium': 1, 'High': 2},
        'Family_Income': {'Low': 0, 'Medium': 1, 'High': 2}
    }
    
    # Apply mapping to categorical columns
    for col, m in mapping.items():
        if col in df.columns:
            # map() will turn the string into the number defined in our dictionary
            # fillna(0) handles cases where a value might be missing or misspelled
            df[col] = df[col].map(m).fillna(0)

    # The model expects exactly 19 features in this specific order
    feature_order = [
        'Hours_Studied', 'Attendance', 'Parental_Involvement', 'Access_to_Resources', 
        'Extracurricular_Activities', 'Sleep_Hours', 'Previous_Scores', 'Motivation_Level', 
        'Internet_Access', 'Tutoring_Sessions', 'Family_Income', 'Teacher_Quality', 
        'School_Type', 'Peer_Influence', 'Physical_Activity', 'Learning_Disabilities', 
        'Parental_Education_Level', 'Distance_from_Home', 'Gender'
    ]
    
    # Ensure only the necessary columns are passed to the scaler
    X = df[feature_order]
    
    # Scale and Predict
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    
    # Return a single rounded float for dict, or array for DataFrame
    if isinstance(data, dict):
        return round(float(prediction[0]), 2)
    return prediction