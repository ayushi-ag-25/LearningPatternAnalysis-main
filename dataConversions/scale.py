import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import csv
def scale(input_file, output_file):
    # 1. Load the numerically mapped data
    df = pd.read_csv(input_file)
    
    # 2. Invert "Negative" features so that 1.0 always = "Better for Success"
    # Distance: Near(0) is better than Far(2) -> Invert
    # Disabilities: No(0) is better than Yes(1) -> Invert
    df['Distance_from_Home'] = df['Distance_from_Home'].max() - df['Distance_from_Home']
    df['Learning_Disabilities'] = df['Learning_Disabilities'].max() - df['Learning_Disabilities']

    # 3. Scale all 19 predictors between 0 and 1
    # This ensures a "high score" in one category (like Previous_Scores 0-100) 
    # doesn't drown out a binary category (like Internet_Access 0-1).
    scaler = MinMaxScaler()
    df[df.columns] = scaler.fit_transform(df[df.columns])
    df.to_csv(output_file,index=False)
scale("processeddata.csv","scaleddata.csv")

