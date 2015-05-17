from django.db import models

class Metricinfo_Table(models.Model):
	Info_ID = models.CharField(max_length=100)
	Title = models.CharField(max_length=100)
	Description = models.CharField(max_length=100)
	Supported = models.CharField(max_length=100)
	Power = models.CharField(max_length=100)
	Mininterval = models.CharField(max_length=100)
	Maxrange = models.CharField(max_length=100)
	Resolution = models.CharField(max_length=100)
	Type = models.CharField(max_length=100)

	class Meta:
		unique_together = (('Info_ID','Title', 'Description','Supported','Power','Mininterval','Maxrange','Resolution','Type'),)

class Metric_Table(models.Model):
	Metric_ID = models.CharField(max_length=100)
	Metric = models.CharField(max_length=100)
	Info_ID = models.CharField(max_length=100)
	Units = models.CharField(max_length=100)
	Max = models.CharField(max_length=100)

	class Meta:
		unique_together = (('Metric_ID','Metric', 'Info_ID','Units','Max'),)

class Data_Table(models.Model):
	Device_ID = models.CharField(max_length=100)
	Sensor_ID = models.CharField(max_length=100)
	Time_Stamp = models.CharField(max_length=100)
	Value = models.CharField(max_length=1000)

	#class Meta:
		#unique_together = (('Device_ID', 'Sensor_ID','Time_Stamp','Value'),)

	def __unicode__(self):
		return u'%s %s %s %s' % (self.Device_ID, self.Sensor_ID,self.Time_Stamp,self.Value)

class Labeling_History(models.Model):
	Device_ID = models.CharField(max_length=100)
	Start_Time = models.CharField(max_length=100)
	End_Time = models.CharField(max_length=100)
	State = models.CharField(max_length=100)

	class Meta:
		unique_together = (('Device_ID', 'Start_Time','End_Time','State'),)

	def __unicode__(self):
		return u'%s %s %s %s' % (self.Device_ID, self.Start_Time,self.End_Time,self.State)



