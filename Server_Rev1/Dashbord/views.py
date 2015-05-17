from  django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template import Context,RequestContext
from Data_Collection.models import Labeling_History,Data_Table
from django.db.models import Count

def User_Login(request):
    if 'username'  in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user =  authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            print "Login "+username  
            return HttpResponseRedirect('/Dash_Board/')   
    return render(request,"Login_Page.html")

@login_required(login_url='/Login/')
def  Dash_Board(request):
    dataSet = Labeling_History.objects.all()
    userLabeling = {}
    for record in dataSet:
        if record.Device_ID not in userLabeling:
            userLabeling[record.Device_ID] = 0
        userLabeling[record.Device_ID] = userLabeling[record.Device_ID] + 1
    sortedRecords = []
    for key, value in sorted(userLabeling.iteritems(), key=lambda (k,v): (v,k)):
        sortedRecords.append({'ID':key,'Value':value})
    print sortedRecords
    return render_to_response("Dashbord.html",{'sortedRecords':sortedRecords},context_instance=RequestContext(request))   

@login_required(login_url='/Login/')
def User_Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/Login/') 

@login_required(login_url='/Login/')
def individualHistory(request,id):
    individualHistory = Labeling_History.objects.filter(Device_ID = str(id)).order_by('Start_Time')
    labelRecords = []
    for record in individualHistory:
        labelRecords.append({'ID':record.Device_ID,'Start_Time':record.Start_Time,'End_Time':record.End_Time,'Activity':record.State})
    sensorHistory =  Data_Table.objects.filter(Device_ID=str(id)).order_by("Time_Stamp")
    sensorRecords = []
    for record in sensorHistory:
        sensorRecords.append({'ID':record.Device_ID,'Sensor':record.Sensor_ID,'Value':record.Value,'Time_Stamp':record.Time_Stamp})
    records = {'labelRecords':labelRecords,'sensorRecords':sensorRecords}
    return render_to_response("IndividualHistory.html",{'sortedRecords':records},context_instance=RequestContext(request))



