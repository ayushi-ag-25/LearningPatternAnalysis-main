# dependencies
reference_dict = {"Hours_Studied": {"min": 1.0, "max": 44.0},
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
    "Exam_Score": {"min": 55.0, "max": 101.0}}

# 3 cluster model centroids
centroid3={'cluster1': [0.26407826, 0.4980978 ], 'cluster2': [0.28523119, 0.83384127], 'cluster3': [0.24843434, 0.16748274]}

# 5 cluster model centroids
centroid5={'cluster1': array([0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936]), 'cluster2': array([0.4705168 , 0.51762281, 0.72973323, 0.31982215, 0.69597686]), 'cluster3': array([0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401]), 'cluster4': array([0.47551055, 0.50872846, 0.34926632, 0.67422251, 0.72645642]), 'cluster5': array([0.4701202 , 0.51256057, 0.55062768, 0.58281026, 0.38376831])}



# the function that converts raw data to numbers
# does it work if Exam_score column is missing? yes imo
def numerical_mapping(record):
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

        # generate mapping
        for i in record.keys():
            if i in mapping_dict:
               record[i]=mapping_dict[i][record[i]]
            else:
                pass
        return(record)

# the function that scales all the numeric values between 0 and 1
def scale(numeric_record):
    for i in numeric_record.keys():
                numeric_record[i] = (numeric_record[i] - reference_dict[i]["min"]) / (reference_dict[i]["max"] - reference_dict[i]["min"])
    return numeric_record

# the function that gets data ready for 3 cluster model
def datafor3(scaled_data):
    academic_rec={}
    academic_rec["Previous_Scores"]=numeric_record["Previous_Scores"]
    academic_rec["Exam_Score"]=numeric_record["Exam_Score"]
    return academic_rec

# the function that gets data ready for 5 cluster model
def datafor5(scaled_data):
    # 1. Invert negative impact features (so 1.0 = Better for Success)
    # Distance: Far (1.0) becomes 0.0 | Learning Disability: Yes (1.0) becomes 0.0
    dist_inv = 1.0 - scaled_data.get('Distance_from_Home', 0)
    disab_inv = 1.0 - scaled_data.get('Learning_Disabilities', 0)
    
    # 2. Calculate the 5 Thematic Features
    
    # Theme 1: Academic Drive (Effort & Motivation)
    academic_drive = (
        scaled_data.get('Hours_Studied', 0) + 
        scaled_data.get('Attendance', 0) + 
        scaled_data.get('Previous_Scores', 0) + 
        scaled_data.get('Motivation_Level', 0)
    ) / 4
    
    # Theme 2: Resource Access (Socio-economic & School Tools)
    resource_access = (
        scaled_data.get('Access_to_Resources', 0) + 
        scaled_data.get('Internet_Access', 0) + 
        scaled_data.get('Tutoring_Sessions', 0) + 
        scaled_data.get('Family_Income', 0) + 
        scaled_data.get('Teacher_Quality', 0) + 
        scaled_data.get('School_Type', 0)
    ) / 6
    
    # Theme 3: Family Capital (Home Support)
    family_capital = (
        scaled_data.get('Parental_Involvement', 0) + 
        scaled_data.get('Parental_Education_Level', 0)
    ) / 2
    
    # Theme 4: Personal Wellbeing (Lifestyle)
    personal_wellbeing = (
        scaled_data.get('Sleep_Hours', 0) + 
        scaled_data.get('Physical_Activity', 0) + 
        scaled_data.get('Extracurricular_Activities', 0)
    ) / 3
    
    # Theme 5: Environmental Stability (External Factors)
    # Uses the inverted values for Distance and Disabilities
    environmental_stability = (
        scaled_data.get('Peer_Influence', 0) + 
        dist_inv + 
        disab_inv
    ) / 3
    
    return {
        "Academic_Drive": academic_drive,
        "Resource_Access": resource_access,
        "Family_Capital": family_capital,
        "Personal_Wellbeing": personal_wellbeing,
        "Environmental_Stability": environmental_stability
    }



# the logic of predict function for both cases when we deal with 19 col or 20 col
def predict(record):
    def twenty_attributes(record):
        # record must be a 20 attribute dictionary
        # 3 group clustering aka academic_performance cluster
        data3=datafor3(scale(numerical_mapping(record)))
        dis3=[] #---> here the square of distances bw each centroids and datapoint is stored
        for i in centroid3.keys():
            prev=data["Previous_Scores"]
            exam=data["Exam_Score"]
            feature1=centroid3[i][0]
            feature2=centroid3[i][1]
            dis3.append((prev-feature1)**2+(exam-feature2)**2)
        ac=dis3.index(min(dis3))+1 
        # ac is academic performance cluster number
      

        # 5 group clustering aka persona clustering
        data5=datafor5(scale(numerical_mapping(record)))
        dis5=[]
        for i in centroid5.keys():
            p=0
            for j in range(5): #--> since we have 5 feature lists
                p+=(centroid5[i][j]-data5[j])**2
            dis5.append(p)
        pc=dis5.index(min(dis5))+1
        # pc is persona cluster number

        return {"academic_performance_cluster_number":ac,"persona_cluster_number":pc}
    if record.get("Exam_Score"):
        twenty_attributes()
    else:
        # we need to see what kind of data Mayank's model takes as input
        # we will make another function to execute that conversion
        # then we write a code to predict the final score of the student
        # then we append that score and the key "Exam_Score" to the record dictionary and then run twenty_attributes()
        pass




# the output we return to be passed to genai

