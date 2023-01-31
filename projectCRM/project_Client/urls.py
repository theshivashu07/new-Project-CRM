from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),
		path('clientdetails/',views.clientdetails,name='clientdetails'),
		path('projectdetails/',views.projectdetails,name='projectdetails'),
		path('projectdetails/<slug:projectslug>',views.projectdetails,name='projectdetails'),
		path('clientconnections/',views.clientconnections,name='clientconnections'),
		path('clientdeactivate/',views.clientdeactivate,name='clientdeactivate'),
		path('clientnotification/',views.clientnotification,name='clientnotification'),
		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		path('activeprojects/@<str:username>',views.reportsopen,name='reportsopen'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('completedprojects/@<str:username>',views.projectdetailsopen,name='projectdetailsopen'),
		# path('trial/',views.trial,name='trial'),
		
]





