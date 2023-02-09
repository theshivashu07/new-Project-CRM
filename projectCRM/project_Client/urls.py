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
		path('activeprojects/latestreport/<slug:projectslug>',views.reportsopen,name='reportsopen'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('projectdetails/completed/<slug:projectslug>',views.completedprojectdetails,name='projectdetailsopen'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		# path('allsuggestions/',views.allsuggestions,name='allsuggestions'),
		path('allmessages/',views.allmessages,name='allmessages'),
		
		# path('trial/',views.trial,name='trial'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		
]





