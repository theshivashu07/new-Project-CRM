"""projectCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [  
    path('defaultadmin/', admin.site.urls),  
    # path('',include('project_Guest.urls')),  
    path('guest/',include('project_Guest.urls')),  # Done  
    # path('',include('project_HR.urls')),  
    path('hr/',include('project_HR.urls')),  # Done  
    # path('',include('project_Admin.urls')),  
    path('admin/',include('project_Admin.urls')),   # Done  
    path('',include('project_ProjectManager.urls')),  
    path('projectmanager/',include('project_ProjectManager.urls')),  
    path('developer/',include('project_Developer.urls')),  
    # path('',include('project_Client.urls')),  
    path('client/',include('project_Client.urls')),  # Done  
]





