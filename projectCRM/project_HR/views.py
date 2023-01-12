from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>HR</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/hr/index.html");

def myaccount(request):
	return render(request,"otherapps/hr/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/hr/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/hr/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/hr/mynotification.html");

def projectsoftdetails(request):
	return render(request,"otherapps/hr/projectsoftdetails.html");

def allprojectsrequests(request):
	return render(request,"otherapps/hr/allprojectsrequests.html");

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/hr/allprojects.html");
def completedprojects(request):
	return render(request,"otherapps/hr/allprojects.html");

# new 
def recruitadmin(request):
	return render(request,"otherapps/hr/recruitadmin.html");
def recruitprojectmanager(request):
	return render(request,"otherapps/hr/recruitprojectmanager.html");
def recruitdeveloper(request):
	return render(request,"otherapps/hr/recruitdeveloper.html");
def promotedeveloper(request):
	return render(request,"otherapps/hr/promotedeveloper.html");
def promoteprojectmanager(request):
	return render(request,"otherapps/hr/promoteprojectmanager.html");

def alldiscussions(request):
	return render(request,"otherapps/hr/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/hr/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/hr/allmessages.html");




