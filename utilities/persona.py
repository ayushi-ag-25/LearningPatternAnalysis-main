import pandas as pd
from math import sqrt

# Define the theme mappings globally for easy maintenance
THEME_MAP = {
    'Academic_Drive': [
        'Hours_Studied', 'Attendance', 'Previous_Scores', 'Motivation_Level'
    ],
    'Resource_Access': [
        'Access_to_Resources', 'Internet_Access', 'Tutoring_Sessions', 
        'Family_Income', 'Teacher_Quality', 'School_Type'
    ],
    'Family_Capital': [
        'Parental_Involvement', 'Parental_Education_Level'
    ],
    'Personal_Wellbeing': [
        'Sleep_Hours', 'Physical_Activity', 'Extracurricular_Activities'
    ],
    'Environmental_Stability': [
        'Peer_Influence', 'Distance_from_Home', 'Learning_Disabilities'
    ]
}

def reduce_dataframe(scaled_df):
    """
    Reduces a full DataFrame of 20 attributes to 5 thematic features.
    Used for batch CSV uploads on the dashboard.
    """
    reduced_df = pd.DataFrame()

    for theme, columns in THEME_MAP.items():
        # Ensure only columns that exist in the DF are used
        existing_cols = [c for c in columns if c in scaled_df.columns]
        if existing_cols:
            reduced_df[theme] = scaled_df[existing_cols].mean(axis=1)
        else:
            reduced_df[theme] = 0.0 # Fallback if no columns found

    # Keep Exam_Score if it exists in the input
    if 'Exam_Score' in scaled_df.columns:
        reduced_df['Exam_Score'] = scaled_df['Exam_Score']
        
    return reduced_df

def reduce_record(scaled_record):
    """
    Reduces a single student dictionary to 5 thematic features.
    Used for single-student lookups/forms in the dashboard.
    """
    reduced_record = {}

    for theme, columns in THEME_MAP.items():
        # Get values for the columns in this theme, default to 0 if missing
        values = [scaled_record.get(col, 0) for col in columns]
        # Calculate mean
        reduced_record[theme] = sum(values) / len(values)

    # Carry over the Exam_Score for reference if provided
    if 'Exam_Score' in scaled_record:
        reduced_record['Exam_Score'] = scaled_record['Exam_Score']

    return reduced_record


# this function is for prediction on dataframes not single record
def predict_pc(data5, centroid5):
    # 1. Initialize output dictionary
    # Example: {"cluster1": [indices], "cluster2": [indices]...}
    persona_map = {cluster: [] for cluster in centroid5.keys()}

    def calcdistance(x, y):
        return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

    # 2. Iterate through the 5-theme dataframe
    for index, row in data5.iterrows():
        # Theme order must match your centroid training order
        point = [
            row['Academic_Drive'], 
            row['Resource_Access'], 
            row['Family_Capital'], 
            row['Personal_Wellbeing'], 
            row['Environmental_Stability']
        ]
        
        best_cluster = None
        mindistance = float('inf')
        
        # 3. Find the closest Persona centroid
        for cluster_name, centroid_coords in centroid5.items():
            dist = calcdistance(point, centroid_coords)
            if dist < mindistance:
                mindistance = dist
                best_cluster = cluster_name
        
        # 4. Store the original index
        persona_map[best_cluster].append(index)
        
    return persona_map
    # this is a dictionary 