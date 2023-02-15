from django.urls import path
from . import views

urlpatterns=[

		path('',views.index,name='index'),

		path('myaccount/',views.myaccount,name='myaccount'),
		path('mynotification/',views.mynotification,name='mynotification'),
		path('myconnections/',views.myconnections,name='myconnections'),
		path('mydeactivate/',views.mydeactivate,name='mydeactivate'),

		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),
		path('projectdetails/',views.projectdetails,name='projectdetails'),
		path('projectdetails/new/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),
		path('projectdetails/edits/<slug:projectslug>',views.projectdetailsedit,name='projectdetailsedit'),

		path('latestreport/<slug:projectslug>',views.latestreport,name='latestreport'),
		path('projectdetails/active/<slug:projectslug>',views.completedprojectdetails,name='completedprojectdetails'),
		path('projectdetails/completed/<slug:projectslug>',views.completedprojectdetails,name='completedprojectdetails'),

		path('activeprojects/',views.activeprojects,name='activeprojects'),
		path('activeprojects/@<str:username>',views.activeprojects,name='activeprojects'),
		path('completedprojects/',views.completedprojects,name='completedprojects'),
		path('completedprojects/@<str:username>',views.completedprojects,name='completedprojects'),

		# new
		path('newjoinees/@<str:username>',views.newjoinees,name='newjoinees'),
		path('recruitments/',views.recruitments,name='recruitments'),
		path('promotions/@<str:username>',views.promotions,name='promotions'),
		path('increments/@<str:username>',views.increments,name='increments'),
		path('decrements/@<str:username>',views.decrements,name='decrements'),
		path('listof/<str:target>/',views.listof,name='listof'),

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),
		# path('allsuggestions/',views.allsuggestions,name='allsuggestions'),
		path('allmessages/',views.allmessages,name='allmessages'),

		# path('trialcenter/<str:key>',views.trialcenter,name='trialcenter'),
		#path('/',views.,name=''),
]


'''
letsrecruit
letspromote
letsincrement
'''





