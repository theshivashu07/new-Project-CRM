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
	return render(request,"otherapps/hr/activeprojects.html");
def completedprojects(request):
	return render(request,"otherapps/hr/completedprojects.html");

# new 
def recruitments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/hr/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/hr/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/hr/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/hr/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/hr/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/hr/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/hr/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/hr/allmessages.html");




