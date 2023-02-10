from django.urls import path
from . import views

urlpatterns=[

		path('',views.index,name='index'),

		path('myaccount/',views.myaccount,name='myaccount'),
		path('myconnections/',views.myconnections,name='myconnections'),
		path('mydeactivate/',views.mydeactivate,name='mydeactivate'),
		path('mynotification/',views.mynotification,name='mynotification'),

		path('projectdetails/',views.projectdetails,name='projectdetails'),
		path('projectdetails/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),
		path('projectdetails/edits/<slug:projectslug>',views.projectdetailsedit,name='projectdetailsedit'),

		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),

		path('latestreport/<slug:projectslug>',views.latestreport,name='latestreport'),
		path('projectdetails/active/<slug:projectslug>',views.completedprojectdetails,name='completedprojectdetails'),
		path('projectdetails/completed/<slug:projectslug>',views.completedprojectdetails,name='completedprojectdetails'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		# path('allsuggestions/',views.allsuggestions,name='allsuggestions'),
		path('allmessages/',views.allmessages,name='allmessages'),

		path('reportscollection/',views.reportscollection,name='reportscollection'),
		# path('wantreports/',views.wantreports,name='wantreports'),
		path('sendreports/',views.sendreports,name='sendreports'),
		path('creativeteam/',views.creativeteam,name='creativeteam'),
		path('sendreports/@<str:username>',views.sendreportsopen,name='sendreportsopen'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),

]


'''
letsrecruit
letspromote
letsincrement
'''



