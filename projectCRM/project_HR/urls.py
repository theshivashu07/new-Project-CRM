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
		path('activeprojects/@<str:username>',views.reportsopen,name='reportsopen'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('completedprojects/@<str:username>',views.projectdetails,name='projectdetails'),

		# new
		path('recruitments/',views.recruitments,name='recruitments'),
		path('promotions/',views.promotions,name='promotions'),
		path('increments/',views.increments,name='increments'),
		path('decrements/',views.decrements,name='decrements'),
		path('pick/<str:target>/',views.pick,name='pick'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		path('allsuggestions/',views.allsuggestions,name='allsuggestions'),
		path('allmessages/',views.allmessages,name='allmessages'),

		# path('trialcenter/',views.trialcenter,name='trialcenter'),
		#path('/',views.,name=''),
]


'''
letsrecruit
letspromote
letsincrement
'''





