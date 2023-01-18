from django.urls import path
from . import views

urlpatterns=[

		path('',views.index,name='index'),

		path('myaccount/',views.myaccount,name='myaccount'),
		path('myconnections/',views.myconnections,name='myconnections'),
		path('mydeactivate/',views.mydeactivate,name='mydeactivate'),
		path('mynotification/',views.mynotification,name='mynotification'),

		path('projectsoftdetails/',views.projectsoftdetails,name='projectsoftdetails'),

		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		path('allsuggestions/',views.allsuggestions,name='allsuggestions'),
		path('allmessages/',views.allmessages,name='allmessages'),

		# path('createteam/',views.createteam,name='createteam'),
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





