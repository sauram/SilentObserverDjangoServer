from django.http import HttpResponse, JsonResponse
from django.http.response import FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from . import models
from . import serializers


@csrf_exempt
def sensor_data(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        sensorDatas = models.SensorData.objects.all()
        serializer = serializers.SensorDataSerializer(sensorDatas, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        #serializer = serializers.SensorDataSerializer(data=data)
        
        return JsonResponse({"response":"server is working"}, status=201, safe= False)
        