import os
import requests
import json
import time
from flask import Flask, jsonify, request, render_template
from utilities import analyze


app = Flask(__name__)

# This pulls the key from Render's environment variables (which we obviously need to set , "let's generate a new one" ). 
# It keeps our API key safe and off of GitHub.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def get_ai_insight(data_summary):
    """Calls Gemini API to generate structured pedagogical insights with exponential backoff."""
    if not GEMINI_API_KEY:
        return "<h3>⚠️ Configuration Needed</h3><ul><li><b>Note:</b> AI insights are currently unavailable because the API Key is not configured on the server.</li></ul>"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"
    
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

    <h3>💡 Recommended Strategies</h3>
    <ul>
        <li><b>Immediate Action:</b> [One specific intervention the teacher should do this week]</li>
        <li><b>Long-term Support:</b> [How to sustain or improve this trajectory over the semester]</li>
    </ul>
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Exponential Backoff for production stability
    for i in range(5):
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 429: # Rate limit
                time.sleep(2**i)
            else:
                break
        except Exception:
            time.sleep(2**i)

    return "<h3>⚠️ Insight Delay</h3><ul><li>The AI advisor is currently processing a high volume of requests. Please review the raw charts above and try again in a moment.</li></ul>"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/analyzeGroup", methods=["POST"])
def analyze_group():
    file = request.files["csv_file"]
    analysis_results = analyze.visualise(file)
    
    summary = {
        "type": "batch",
        "clusters": analysis_results['charts']['academic_distribution']
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    return jsonify(analysis_results)

@app.route("/analyzeStudent", methods=["POST"])
def analyze_student():
    data = request.form.to_dict()
    numeric_keys = ["Hours_Studied", "Attendance", "Sleep_Hours", "Previous_Scores", "Tutoring_Sessions", "Physical_Activity","Exam_Score"]
    
    for key in numeric_keys:
        if key in data and data[key]:
            try:
                data[key] = float(data[key])
            except ValueError:
                data[key] = 0.0

    analysis_results = analyze.visualise(data)
    
    summary = {
        "type": "single",
        "predicted_score": analysis_results.get('score_value', 'N/A'),
        "metrics": data
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    return jsonify(analysis_results)

if __name__ == "__main__":
    app.run(debug=True)
