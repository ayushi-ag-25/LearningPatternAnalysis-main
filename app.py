import os
import requests
import json
from flask import Flask, jsonify, request, render_template
from utilities import analyze


app = Flask(__name__)

# CONFIGURATION: Set your API Key here or as an environment variable
GEMINI_API_KEY = "AIzaSyBGE2sH8HbpK877YlHWq0ajwHmxFfeX5fc" #enter a value here at runtime

def get_ai_insight(data_summary):
    """Calls Gemini API to generate structured pedagogical insights using HTML formatting."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"
    
    # We define a strict template to ensure the UI looks consistent
    prompt = f"""
    As an AI Education Consultant, analyze this JSON data: {json.dumps(data_summary)}
    
    Your goal is to provide a structured, high-impact report for a teacher. 
    You MUST format your response using ONLY the following HTML tags: <h3>, <ul>, <li>, and <b>.
    Do NOT use Markdown (no # or **).

    Structure your response exactly like this:
    
    <h3>🎯 Key Observations</h3>
    <ul>
        <li><b>Trend Analysis:</b> [1 sentence on the overall academic direction of the group/student]</li>
        <li><b>Metric Highlight:</b> [Identify the most significant contributing factor from the data]</li>
    </ul>

    <h3>💡 Strategic Recommendations</h3>
    <ul>
        <li><b>Immediate Action:</b> [One specific step the teacher should take tomorrow]</li>
        <li><b>Long-term Support:</b> [How to sustain or fix the current trend]</li>
        <li><b>Resource Optimization:</b> [How to use tutoring or study hours more effectively based on this specific data]</li>
    </ul>

    <h3>⚠️ Risk Assessment</h3>
    <ul>
        <li>[Identify one major red flag or "Declining" cluster risk if applicable]</li>
    </ul>
    
    Keep the tone professional, data-driven, and concise.
    """
    
    payload = {
        "contents": [{ "parts": [{ "text": prompt }] }]
    }
    
    # Retry logic with exponential backoff
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                # Extracting the generated text
                text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            
        import time
        time.sleep(delay)
    
    return "<h3>Notice</h3><ul><li>Insights are temporarily unavailable. Please review the raw charts above.</li></ul>"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/analyzeGroup", methods=["POST"])
def analyze_group():
    file = request.files["csv_file"]
    analysis_results = analyze.visualise(file)
    
    # Generate AI insights based on the analysis
    summary = {
        "type": "batch",
        "clusters": analysis_results['charts']['academic_distribution']
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    return jsonify(analysis_results)

@app.route("/analyzeStudent", methods=["POST"])
def analyze_student():
    data = request.form.to_dict()
    # this thing 
    numeric_keys = ["Hours_Studied", "Attendance", "Sleep_Hours", "Previous_Scores", "Tutoring_Sessions", "Physical_Activity","Exam_Score"]
    
    for key in numeric_keys:
        if key in data and data[key]:
            try:
                data[key] = float(data[key])
            except ValueError:
                data[key] = 0.0

    analysis_results = analyze.visualise(data)
    
    # Generate AI insights for single student
    summary = {
        "type": "single",
        "predicted_score": analysis_results['score_value'],
        "metrics": analysis_results['charts']['spider_chart']['data']
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    return jsonify(analysis_results)
    

if __name__ == "__main__":
    app.run(debug=True) 
