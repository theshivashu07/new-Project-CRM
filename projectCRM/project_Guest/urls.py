from django.urls import path
from . import views

urlpatterns=[
		path('',views.index,name='index'),
		path('index/',views.index,name='index'),
		path('workprocess/',views.workprocess,name='workprocess'),
		path('aboutus/',views.aboutus,name='aboutus'),
		path('contactus/',views.contactus,name='contactus'),
		# path('admin/login/',views.loginMethod,name='login',),
		# path('projectmanager/login/',views.loginMethod,name='login'),
		# path('developer/login/',views.loginMethod,name='login'),
		path('login/',views.loginMethod,name='login'),
		path('visit/',views.visit,name='visit'),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		#path('/',views.,name=''),
		
]







