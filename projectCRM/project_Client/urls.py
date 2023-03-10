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
		path('projectdetails/edits/<slug:projectslug>',views.projectdetailsedit,name='projectdetailsedit'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		# path('activeprojects/latestreport/<slug:projectslug>',views.latestreport,name='latestreport'),
		path('latestreport/<slug:projectslug>',views.latestreport,name='latestreport'),  #✓
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('projectdetails/active/<slug:projectslug>',views.completedprojectdetails,name='activeprojectdetails'),
		path('projectdetails/completed/<slug:projectslug>',views.completedprojectdetails,name='projectdetailsopen'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		path('allmessages/',views.allmessages,name='allmessages'),

		path('reportscollection/',views.reportscollection,name='reportscollection'),  #✓
		
		# path('trial/',views.trial,name='trial'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		
]




