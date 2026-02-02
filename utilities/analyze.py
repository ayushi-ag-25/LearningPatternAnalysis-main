
import pandas as pd
from math import sqrt
import os
import json

try:
    from . import preprocessing
    from . import academics
    from . import persona
    from . import predict_score
except ImportError:
    import preprocessing
    import academics
    import persona
    import predict_score

# 3-cluster model centroids (Academic Performance)
CENTROID3 = {
    'cluster1': [0.26407826, 0.4980978], # Yellow (Baseline)
    'cluster2': [0.28523119, 0.83384127], # Green (High Growth)
    'cluster3': [0.24843434, 0.16748274]  # Red (Critical)
}

# 5-cluster model centroids (Behavioural Personas)
CENTROID5 = {
    'cluster1': [0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936], 
    'cluster2': [0.47051680, 0.51762281, 0.72973323, 0.31982215, 0.69597686], 
    'cluster3': [0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401], 
    'cluster4': [0.47050352, 0.52125862, 0.34757303, 0.67812502, 0.73516515],
    'cluster5': [0.48512111, 0.51239632, 0.34586241, 0.32626084, 0.23126512]
}

def get_complete_analysis(data):
    """
    Coordination logic to get predictions and cluster assignments.
    """
    if isinstance(data, dict):
        raw_record = data.copy()
        is_predicted = False
        
        # Check if score needs prediction
        if 'Exam_Score' not in raw_record or raw_record['Exam_Score'] is None or raw_record['Exam_Score'] == "":
            raw_record['Exam_Score'] = predict_score.predict_exam_score(raw_record)
            is_predicted = True
        
        scaled_record = preprocessing.scale_single_record(raw_record)
        
        # Phase 1: We still calculate reduced data for the spider chart
        reduced = persona.reduce_record(scaled_record)
        
        return {
            "mode": "single",
            "predicted_score": raw_record['Exam_Score'],
            "is_predicted": is_predicted,
            "radar_data": reduced,
            "scaled_data": scaled_record
        }

    else:
        # Batch behavior remains as it is (Phase 1 group analysis)
        if isinstance(data, str):
            df = pd.read_csv(data)
        else:
            df = data.copy()

        is_predicted = False
        if 'Exam_Score' not in df.columns or df['Exam_Score'].isnull().any():
            df['Exam_Score'] = predict_score.predict_exam_score(df)
            is_predicted = True
            
        processed_df = preprocessing.scale_csv_file(df)
        
        data3_df = academics.pick2rec(processed_df)
        ac_map = academics.predict_ac(data3_df, CENTROID3)
        
        data5_df = persona.reduce_dataframe(processed_df)
        pc_map = persona.predict_pc(data5_df, CENTROID5)
        
        return {
            'score':df['Exam_Score'],
            "mode": "batch",
            "is_predicted": is_predicted,
            "academic_mapping": ac_map,
            "persona_mapping": pc_map,
            "full_df": processed_df,
            "reduced_df": data5_df
        }

def visualise(data):
    """
    Transforms analysis results into structured data for UI charts.
    Follows Phase 1 logic: Single student only shows Prediction + Spider Chart.
    """
    analysis = get_complete_analysis(data)
    
    if analysis['mode'] == 'single':
        # Result container
        result = {
            "type": "single",
            "is_predicted_score": analysis['is_predicted'],
            "charts": {
                "spider_chart": {
                    "data": [
                        {"subject": k.replace('_', ' '), "value": round(v * 100, 2)} 
                        for k, v in analysis['radar_data'].items()
                    ]
                }
            }
        }
        
        # Phase 1 Logic: Only include score value if it was predicted 
        # (or if you want to show provided score, keep it here)
        if analysis['is_predicted']:
            result["score_value"] = round(analysis['predicted_score'], 2)
        else:
            # If score was provided, the plan says return "5featurespiderchart" only
            # but usually, dashboards still display the input score for context.
            result["score_value"] = round(analysis['predicted_score'], 2)

        return result
    
    else:
        # Batch mode (Whole Group) behavior remains unchanged
        ac_map = analysis['academic_mapping']
        pc_map = analysis['persona_mapping']
        total_students = sum(len(v) for v in ac_map.values())

        academic_pie = [
            {"name": k, "value": len(v), "percentage": round((len(v)/total_students)*100, 2)}
            for k, v in ac_map.items()
        ]

        persona_pie = [
            {"name": k, "value": len(v), "percentage": round((len(v)/total_students)*100, 2)}
            for k, v in pc_map.items()
        ]

        nested_breakdown = {}
        for ac_key, ac_indices in ac_map.items():
            breakdown = []
            for pc_key, pc_indices in pc_map.items():
                intersection = set(ac_indices).intersection(set(pc_indices))
                if intersection:
                    breakdown.append({
                        "persona": pc_key,
                        "count": len(intersection),
                        "percentage": round((len(intersection)/len(ac_indices))*100, 2)
                    })
            nested_breakdown[ac_key] = breakdown

        return {
            "type": "batch",
            "is_predicted_batch": analysis['is_predicted'],
            "charts": {
                "academic_distribution": academic_pie,
                "overall_persona_distribution": persona_pie,
                "persona_per_academic_cluster": nested_breakdown
            }
        }

