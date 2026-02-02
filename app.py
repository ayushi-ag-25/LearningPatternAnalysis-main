from flask import *

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def pre():
    #from utilities import get_complete_analysis
    #data=request.json()
    #anlyzdata=get_complete_analysis(data)
    out={'content':'abc'}
    
    return jsonify(out)

@app.route('/csvanalyze',methods=['POST','GET'])
def csvv():
    file = request.files["csv_file"]
    model = request.form["model"]
    #work in progresss

app.run(debug=True)


