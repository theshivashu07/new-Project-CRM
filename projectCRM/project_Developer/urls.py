from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),
		path('allprojects',views.allprojects,name='allprojects'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		
]



