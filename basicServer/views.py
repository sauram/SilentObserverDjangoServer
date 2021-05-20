from django.http import HttpResponse, JsonResponse
from django.http.response import FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from . import models
from . import serializers
from tensorflow import keras
import numpy as np
import os
import json

def isdirectory(userId):
    dir = f"./SilentObserverServerFileDatabase/User_{userId}"
    return os.path.isdir(dir)

def createDirectory(userId):
    dir = f"./SilentObserverServerFileDatabase/User_{userId}"
    os.makedirs(dir)

def storeData(userID):
    sensorDatas = models.SensorData.objects.filter(userId__exact = userID)
    fileLocation = f"./SilentObserverServerFileDatabase/User_{userID}/{userID}.json"
    '''
    for e in sensorDatas:
        dataDump = {"userId":e.userId, "values": e.values}
        with open(fileLocation,'w') as json_file:
            json.dump(dataDump,json_file)
    '''
    with open(fileLocation,'w') as json_file:
        for e in sensorDatas:
            dataDump = {"userId":e.userId, "values": e.values} 
            json.dump(dataDump,json_file)
    


@csrf_exempt
def make_model(request):
    data = JSONParser().parse(request)
    print(type(data))
    userID = data["userId"]
    if(isdirectory(userID)==False):
        createDirectory(userID)
    storeData(userID)
    #TODO #createModel function to be called
    return JsonResponse({"response": "Started"}, status=201, safe=False)

@csrf_exempt
def result_data(request):
    data = JSONParser().parse(request)

    #segregate the useful data into different variables
    raw_data= data["values"]
    userId = data["userId"]
    
    #for testing purposes
    '''
    raw_data=[]
    for i in range(128*12):
        raw_data.append(random.random())
    '''

    #Process data to use in the model
    processed_data=[]
    for i in range(128):
        temp_list=[]
        for j in range(12):
            temp_list.append(raw_data[i + j*128])
        processed_data.append(temp_list)
    final_data = []
    final_data.append(processed_data)
    np_final_data = np.array(final_data)

    #load model and use the processed data
    dir = f"./SilentObserverServerFileDatabase/User_{userId}/{userId}"
    if(isdirectory(dir)):
        reconstructed_model=keras.models.load_model(dir)
        result= reconstructed_model.predict(np_final_data)
        ans="Malicious"
        if(result[0][0]>result[0][1]):
            ans="Non-Malicious"
    else:
        ans = "Not-Completed"

    print(ans)
    return JsonResponse({"response":ans}, status=201, safe= False)
            
    
@csrf_exempt
def save_data(request):
    data = JSONParser().parse(request)
    serializer = serializers.SensorDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"response":"Working"}, status=201, safe= False)
    return JsonResponse(serializer.errors, status=400)
    
        
        



