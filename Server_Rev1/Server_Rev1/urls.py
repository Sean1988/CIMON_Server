from django.conf.urls import patterns, include, url
from Data_Collection.views import Data_Handler
from Dashbord.views import User_Login,Dash_Board,User_Logout,individualHistory
from django.contrib import admin
from MonitorReport.views import exportReport
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^Update_Data/$', Data_Handler),
	url(r'^Login/$',User_Login),
	url(r'^Logout/$',User_Logout),
	url(r'^Dash_Board/$',Dash_Board),
	url(r'^Report/$',exportReport),
	url(r'^History/(?P<id>\d+)/$',individualHistory),
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^Dash_Bord/$',Dash_Bord),
)
