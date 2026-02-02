import pandas as pd

def map_new_data(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Mapping definitions
    ordinal_map = {'Low': 0, 'Medium': 1, 'High': 2}
    binary_map = {'No': 0, 'Yes': 1}
    school_map = {'Public': 0, 'Private': 1}
    peer_map = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
    edu_map = {'High School': 0, 'College': 1, 'Postgraduate': 2}
    dist_map = {'Near': 0, 'Moderate': 1, 'Far': 2}
    gender_map = {'Female': 0, 'Male': 1}

    # Column configuration
    mapping_dict = {
        'Parental_Involvement': ordinal_map,
        'Access_to_Resources': ordinal_map,
        'Motivation_Level': ordinal_map,
        'Family_Income': ordinal_map,
        'Teacher_Quality': ordinal_map,
        'Extracurricular_Activities': binary_map,
        'Internet_Access': binary_map,
        'Learning_Disabilities': binary_map,
        'School_Type': school_map,
        'Peer_Influence': peer_map,
        'Parental_Education_Level': edu_map,
        'Distance_from_Home': dist_map,
        'Gender': gender_map
    }

    # Apply mapping and handle missing values with -1
    for col, m in mapping_dict.items():
        df[col] = df[col].map(m).fillna(-1).astype(int)

    # Save the numeric dataset
    df.to_csv(output_file, index=False)
    return df

# Run the mapping
map_new_data('rawdata.csv', 'processeddata.csv')