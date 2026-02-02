import pandas as pd

# Global reference for consistent scaling across the whole app
REFERENCE_DICT = {
    "Hours_Studied": {"min": 1.0, "max": 44.0},
    "Attendance": {"min": 60.0, "max": 100.0},
    "Parental_Involvement": {"min": 0.0, "max": 2.0},
    "Access_to_Resources": {"min": 0.0, "max": 2.0},
    "Extracurricular_Activities": {"min": 0.0, "max": 1.0},
    "Sleep_Hours": {"min": 4.0, "max": 10.0},
    "Previous_Scores": {"min": 50.0, "max": 100.0},
    "Motivation_Level": {"min": 0.0, "max": 2.0},
    "Internet_Access": {"min": 0.0, "max": 1.0},
    "Tutoring_Sessions": {"min": 0.0, "max": 8.0},
    "Family_Income": {"min": 0.0, "max": 2.0},
    "Teacher_Quality": {"min": -1.0, "max": 2.0},
    "School_Type": {"min": 0.0, "max": 1.0},
    "Peer_Influence": {"min": 0.0, "max": 2.0},
    "Physical_Activity": {"min": 0.0, "max": 6.0},
    "Learning_Disabilities": {"min": 0.0, "max": 1.0},
    "Parental_Education_Level": {"min": -1.0, "max": 2.0},
    "Distance_from_Home": {"min": -1.0, "max": 2.0},
    "Gender": {"min": 0.0, "max": 1.0},
    "Exam_Score": {"min": 55.0, "max": 101.0}
}

def process_dataframe(df):
    """The core logic that maps, scales, and inverts a whole dataframe."""
    # 1. Mapping
    mapping_dict = {
        'Parental_Involvement': {'Low': 0, 'Medium': 1, 'High': 2},
        'Access_to_Resources': {'Low': 0, 'Medium': 1, 'High': 2},
        'Motivation_Level': {'Low': 0, 'Medium': 1, 'High': 2},
        'Family_Income': {'Low': 0, 'Medium': 1, 'High': 2},
        'Teacher_Quality': {'Low': 0, 'Medium': 1, 'High': 2},
        'Extracurricular_Activities': {'No': 0, 'Yes': 1},
        'Internet_Access': {'No': 0, 'Yes': 1},
        'Learning_Disabilities': {'No': 0, 'Yes': 1},
        'School_Type': {'Public': 0, 'Private': 1},
        'Peer_Influence': {'Negative': 0, 'Neutral': 1, 'Positive': 2},
        'Parental_Education_Level': {'High School': 0, 'College': 1, 'Postgraduate': 2},
        'Distance_from_Home': {'Near': 0, 'Moderate': 1, 'Far': 2},
        'Gender': {'Female': 0, 'Male': 1}
    }

    # Apply mapping
    for col, m in mapping_dict.items():
        if col in df.columns:
            # We use .get to handle unexpected strings safely
            df[col] = df[col].map(m).fillna(-1)

    # 2. Scaling & Inversion
    for col in df.columns:
        if col in REFERENCE_DICT:
            c_min = REFERENCE_DICT[col]['min']
            c_max = REFERENCE_DICT[col]['max']
            
            # Standard Scaling
            df[col] = (df[col] - c_min) / (c_max - c_min)

            # Inversion for Negative Features
            if col in ['Distance_from_Home', 'Learning_Disabilities']:
                df[col] = 1.0 - df[col]
    
    return df

def scale_csv_file(df):
    """Helper to read a file and process it."""
    
    return process_dataframe(df)

def scale_single_record(record_dict):
    """Helper to process a single student from a dashboard form."""
    df = pd.DataFrame([record_dict])
    processed_df = process_dataframe(df)
    return processed_df.iloc[0].to_dict()