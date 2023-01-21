from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>Admin</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/projectmanager/index.html");

def myaccount(request):
	return render(request,"otherapps/projectmanager/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/projectmanager/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/projectmanager/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/projectmanager/mynotification.html");

def projectsoftdetails(request):
	return render(request,"otherapps/projectmanager/projectsoftdetails.html");

def allprojectsrequests(request):
	return render(request,"otherapps/projectmanager/allprojectsrequests.html");

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/projectmanager/activeprojects.html");
def completedprojects(request):
	return render(request,"otherapps/projectmanager/completedprojects.html");

# new 
def recruitments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/projectmanager/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/projectmanager/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/projectmanager/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/projectmanager/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/projectmanager/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/projectmanager/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/projectmanager/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/projectmanager/allmessages.html");

def reportscollection(request):
	return render(request,"otherapps/projectmanager/reportscollection.html");
def sendreports(request):
	return render(request,"otherapps/projectmanager/sendreports.html");
def sendreportsopen(request,username):
	return render(request,"otherapps/projectmanager/sendreportsopen.html");








