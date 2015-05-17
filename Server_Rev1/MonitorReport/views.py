from  django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template import Context,RequestContext
from Data_Collection.models import Metricinfo_Table,Metric_Table,Data_Table, Labeling_History
import csv
import unicodedata
DownloadOptions = {'tables':[Metricinfo_Table._meta.db_table, Metric_Table._meta.db_table, Data_Table._meta.db_table, Labeling_History._meta.db_table]} 

@login_required(login_url='/Login/')
def exportReport(request):
	if 'table' in request.POST:
		tableName = request.POST['table']
		table = getModel(tableName)
		return getResponse(table)
	return render_to_response("Download_Report.html",DownloadOptions,context_instance=RequestContext(request))   

def getModel(tableName):
	if tableName == Metricinfo_Table._meta.db_table:
		return Metricinfo_Table
        if tableName == Metric_Table._meta.db_table:
                return Metric_Table
	if tableName == Data_Table._meta.db_table:
		return Data_Table
	if tableName == Labeling_History._meta.db_table:
		return Labeling_History

def getResponse(table):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="'+table._meta.db_table+'.csv"'
	writer = csv.writer(response)
	columnNames = table._meta.get_all_field_names()
	dataSet = table.objects.all();
	for record in dataSet:
		row = ""
		for column in columnNames:
			if column == 'id':
				continue
			row = row + getattr(record,str(column)) + '\t'
		row = row + '\n'
		row = unicodedata.normalize('NFKD', row).encode('ascii','ignore')
		print row
		writer.writerow([row])
	return response

