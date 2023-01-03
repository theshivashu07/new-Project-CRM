from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),
		path('clientdetails/',views.clientdetails,name='clientdetails'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		
]



