import pandas as pd
from math import sqrt
def pick2rec(input_data):
    """
    Extracts 'Exam_Score' and 'Previous_Scores' for the 3-cluster model.
    Works for:
    1. A pandas DataFrame (from a CSV)
    2. A single student dictionary (from a dashboard form)
    """
    cols = ['Exam_Score', 'Previous_Scores']
    
    # Case 1: Input is a DataFrame (Full CSV)
    if isinstance(input_data, pd.DataFrame):
        # Verify columns exist to avoid errors
        if all(col in input_data.columns for col in cols):
            return input_data[cols]
        else:
            missing = [c for c in cols if c not in input_data.columns]
            raise KeyError(f"Missing academic columns in DataFrame: {missing}")

    # Case 2: Input is a Dictionary (Single Student)
    elif isinstance(input_data, dict):
        # Extract the two values and return them as a small dictionary or list
        if all(col in input_data for col in cols):
            return {col: input_data[col] for col in cols}
        else:
            missing = [c for c in cols if c not in input_data]
            raise KeyError(f"Missing academic keys in record: {missing}")

    else:
        raise TypeError("Input must be a pandas DataFrame or a dictionary.")

def predict_ac(data3, centroids):
    # 1. Initialize output dictionary
    prediction_map = {cluster: [] for cluster in centroids.keys()}
    
    def calcdistance(x, y):
        # Euclidean distance formula
        return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

    # 2. Iterate through the dataframe by index
    for index, row in data3.iterrows():
        point = [row['Exam_Score'], row['Previous_Scores']]
        
        best_cluster = None
        min_dist = float('inf')
        
        # 3. Find the closest centroid
        for cluster_name, centroid_coords in centroids.items():
            dist = calcdistance(point, centroid_coords)
            if dist < min_dist:
                min_dist = dist
                best_cluster = cluster_name
        
        # 4. Store the index (e.g., if it's record 13, index is 12)
        prediction_map[best_cluster].append(index)
        
    return prediction_map
    # returns a dictionary