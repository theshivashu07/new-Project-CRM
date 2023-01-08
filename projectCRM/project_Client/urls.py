from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),
		path('clientdetails',views.clientdetails,name='clientdetails'),
		path('projectsoftdetails',views.projectsoftdetails,name='projectsoftdetails'),
		path('clientconnections',views.clientconnections,name='clientconnections'),
		path('clientdeactivate',views.clientdeactivate,name='clientdeactivate'),
		path('clientnotification',views.clientnotification,name='clientnotification'),
		#path('/',views.,name=''),
		
]



