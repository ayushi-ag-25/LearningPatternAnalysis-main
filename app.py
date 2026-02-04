from flask import Flask, jsonify, request , render_template
import pandas as pd

app = Flask(__name__)

def analyze(df):
    return {
        "bar1": {
            "labels": ["Low", "Medium", "High"],
            "datasets": [{
                "label": "Student Performance",
                "data": [20, 35, 15],
                "backgroundColor": ["#ff6384", "#36a2eb", "#ffce56"]
            }]
        },
        "bar2": {
            "labels": ["Math", "Science", "English"],
            "datasets": [{
                "label": "Subject Avg",
                "data": [70, 75, 68],
                "backgroundColor": ["#4bc0c0", "#9966ff", "#ff9f40"]
            }]
        },
        "pie1": {
            "labels": ["Cluster A", "Cluster B", "Cluster C"],
            "datasets": [{
                "data": [40, 35, 25],
                "backgroundColor": ["#36a2eb", "#ff6384", "#ffce56"]
            }]
        },
        "pie2": {
            "labels": ["Pass", "Fail"],
            "datasets": [{
                "data": [85, 15],
                "backgroundColor": ["#4caf50", "#f44336"]
            }]
        },
        "pie3": {
            "labels": ["Male", "Female"],
            "datasets": [{
                "data": [55, 45],
                "backgroundColor": ["#2196f3", "#e91e63"]
            }]
        },
        "insight": "Most students fall in the medium-performance category."
    }

@app.route('/')
def home():
    return render_template('k.html')


@app.route("/analyze-default")
def analyze_default():
    df = pd.DataFrame()  # placeholder
    return jsonify(analyze(df))

@app.route("/analyze", methods=["POST"])
def analyze_upload():
    file = request.files["csv_file"]
    df = pd.read_csv(file)
    return jsonify(analyze(df))

@app.route('/predict',methods=['POST','GET'])
def pre():
    #from utilities import get_complete_analysis
    #data=request.json()
    #anlyzdata=get_complete_analysis(data)
    out={'content':'abc'}
    
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True)
