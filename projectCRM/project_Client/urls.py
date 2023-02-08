from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),

		path('myaccount/',views.myaccount,name='myaccount'),
		path('mynotification/',views.mynotification,name='mynotification'),
		path('myconnections/',views.myconnections,name='myconnections'),
		path('mydeactivate/',views.mydeactivate,name='mydeactivate'),

		path('projectdetails/',views.projectdetails,name='projectdetails'),
		path('projectdetails/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),
		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		path('activeprojects/@<str:username>',views.reportsopen,name='reportsopen'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('completedprojects/@<str:username>',views.projectdetailsopen,name='projectdetailsopen'),
		# path('trial/',views.trial,name='trial'),
		
]





