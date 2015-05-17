from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Data_Collection.models import Metricinfo_Table,Metric_Table,Data_Table,Labeling_History
import json

import base64
from Crypto.Cipher import AES
from Crypto import Random
import binascii

key = "20E9475FECE29056201406863B7E809F"

@csrf_exempt
def Data_Handler(request):
    data = json.loads(request.body)
    PackageType = data['table']
    if PackageType == 'metricinfo':
        return UpdateMetricinfo_Table(data)
    if PackageType == 'data':
        return UpdateData_Table(data)
    if PackageType == 'labeling_history':
        return UpdateLabelling_History(data)
    if PackageType == 'metrics':
        return UpdateMetric_Table(data)
    if PackageType == 'Test':
        return Test(data)
    return HttpResponse("No such table")

def Test(data):
    arr = json.loads(decrypt(data['records']))
    print str(arr) == str(data['records2'])
    print data
    return HttpResponse("Success")

def decrypt(encoded):
    BLOCK_SIZE = 32
    PADDING = '|'
    cipher = AES.new(key)
    whole = cipher.decrypt(base64.b64decode(encoded)).rstrip(PADDING)
    pad = whole.find("|")
    if pad == -1:
        raise NoPadInString
    return whole[pad+1:]

def UpdateMetricinfo_Table(data):
    try:
        arr = json.loads(decrypt(data['records']))
        for record in arr:
            Info_ID = record['_id']
	    Title = record['title']
            Description = record['description']
            Supported = record['supported']
            Power = record['power']
            Mininterval = record['mininterval']
            Maxrange = record['maxrange']
            Resolution = record['resolution']
            Type = record['type']
            NewSensorGroup = Metricinfo_Table(Info_ID = Info_ID, Title = Title, Description = Description, Supported = Supported, Power = Power, Mininterval = Mininterval, Maxrange = Maxrange, Resolution = Resolution, Type = Type)
            NewSensorGroup.save()
        return HttpResponse("Success")
    except Exception, e: 
        print str(e)
        return HttpResponse("Failed")

def UpdateMetric_Table(data):
    try:
        arr = json.loads(decrypt(data['records']))
        for record in arr:
	    Metric_ID = record['_id']
            Metric = record['metric']
            Infoid = record['infoid']
            Units = record['units']
            Max = record['max']
            NewMetric = Metric_Table(Metric_ID = Metric_ID, Metric = Metric, Info_ID = Infoid, Units = Units, Max = Max)
            NewMetric.save()
        return HttpResponse("Success")
    except Exception, e:
        print str(e)
        return HttpResponse("Failed")

def UpdateData_Table(data):
    try:
        arr = json.loads(decrypt(data['records']))
        Device_ID = data['device_id']
        for record in arr:
            Sensor_ID = record['metricid']
            Value = record['value']
            Time_Stamp = record['timestamp']
            NewMeasure = Data_Table(Device_ID = Device_ID, Sensor_ID = Sensor_ID, Time_Stamp = Time_Stamp, Value = Value)
            NewMeasure.save()
        return HttpResponse("Success")
    except Exception, e:
        print str(e)
        return HttpResponse("Failed")

def UpdateLabelling_History(data):
    try:
        arr = json.loads(decrypt(data['records']))
        Device_ID = data['device_id']
        for record in arr:
            start_time = record['start_time']
            end_time = record['end_time']
            state = record['state']
            NewFreq = Labeling_History(Device_ID=Device_ID, Start_Time = start_time, End_Time = end_time, State = state)
            NewFreq.save()
        return HttpResponse("Success")
    except Exception, e:
        print str(e)
        return HttpResponse("Failed")
