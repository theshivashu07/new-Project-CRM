from django.urls import path
from . import views

urlpatterns=[

		path('',views.index,name='index'),  #✓

		path('myaccount/',views.myaccount,name='myaccount'),  #✓
		path('myconnections/',views.myconnections,name='myconnections'),  #✓
		path('mydeactivate/',views.mydeactivate,name='mydeactivate'),  #✓
		path('mynotification/',views.mynotification,name='mynotification'),  #✓

		path('allprojectsrequests/',views.allprojectsrequests,name='allprojectsrequests'),  #✓
		path('projectdetails/new/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),  #✓
		path('projectdetails/edits/<slug:projectslug>',views.projectdetailsedit,name='projectdetailsedit'),  #✓

		path('activeprojects/',views.activeprojects,name='activeprojects'),  #✓
		path('latestreport/<slug:projectslug>',views.latestreport,name='latestreport'),  #✓
		path('projectdetails/active/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),  #✓

		path('completedprojects/',views.completedprojects,name='completedprojects'),  #✓
		path('projectdetails/completed/<slug:projectslug>',views.projectdetailsslug,name='projectdetailsslug'),  #✓

		path('alldiscussions/',views.alldiscussions,name='alldiscussions'),  #✓
		path('allmessages/',views.allmessages,name='allmessages'),  #✓

		path('reportscollection/',views.reportscollection,name='reportscollection'),  #✓
		path('sendreports/',views.sendreports,name='sendreports'),  #✓
		path('sendreports/<slug:projectslug>',views.sendreportsopen,name='sendreportsopen'),  #✓

		path('assignedtasks/',views.assignedtasks,name='assignedtasks'),  #✓
		path('assignedtasks/<slug:projectslug>',views.assignedtasksopen,name='assignedtasksopen'),  #✓

		#path('/',views.,name=''),
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



