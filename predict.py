# 3 cluster model centroids
centroid3={'cluster1': [0.26407826, 0.4980978 ], 'cluster2': [0.28523119, 0.83384127], 'cluster3': [0.24843434, 0.16748274]}

# 5 cluster model centroids
centroid5={'cluster1': [0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936], 'cluster2': [0.4705168 , 0.51762281, 0.72973323, 0.31982215, 0.69597686], 'cluster3': [0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401], 'cluster4': [0.47551055, 0.50872846, 0.34926632, 0.67422251, 0.72645642], 'cluster5': [0.4701202 , 0.51256057, 0.55062768, 0.58281026, 0.38376831]}


# import the package we built
from utilities import persona, preprocessing,academics


# run the prediction function
def predict(data):
    if type(data)==type({}):
        # we are dealing with one record
        processed_data=preprocessing.scale_single_record(data) 
        #this is a dictionary

        # pass the record to 3 cluster model
        # get data ready
        data3=academics.pick2rec(processed_data)
        # predict
        dis3=[] #---> here the square of distances bw each centroids and datapoint is stored
        for i in centroid3.keys():
            prev=data["Previous_Scores"]
            exam=data["Exam_Score"]
            feature1=centroid3[i][0]
            feature2=centroid3[i][1]
            dis3.append((prev-feature1)**2+(exam-feature2)**2)
        ac=dis3.index(min(dis3))+1
        # ac is academic performance cluster number

        # pass data to 5 cluster model
        # get data ready
        data5=persona.reduce_record(processed_data)
        # predict
        dis5=[]
        for i in centroid5.keys():
            p=0
            for j in range(5): #--> since we have 5 feature lists
                p+=(centroid5[i][j]-data5[j])**2
            dis5.append(p)
        pc=dis5.index(min(dis5))+1
        # pc is persona cluster number
        
        # return final data
        return {"academic_performance":ac,"persona_cluster":pc}


    else:
        # we are dealing with csv
        # pass it through the preprocessing pipeline
        processed_data=preprocessing.scale_csv_file(data)
        # this is a dataframe
        
        # pass it to 3 cluster model
        # ---------getting data ready--------
        data3=academics.pick2rec(processed_data)
        # according to me this is a dataframe
        # ------------predict--------------
        # what kind of output do i want:
        # cluster1=[index of all records belonging to this cluster in the df processed_data like if record 13 is in cluster1 then store its index which is 12]
        ac=academics.predict_ac(data3,centroid3)
        # ac is a dictionary
        
        
        # pass it to 5 cluster model
        data5=persona.reduce_dataframe(processed_data)
        # this too is a dataframe 
        # ------------predict--------------
        # output format is same as in case of 3 cluster
        pc=persona.predict_pc(data5,centroid5)

        # not sure of what to return



# what we send to the genai
# def gen_ai()

