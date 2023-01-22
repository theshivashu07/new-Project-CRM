from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>Admin</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/admin/index.html");

def myaccount(request):
	return render(request,"otherapps/admin/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/admin/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/admin/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/admin/mynotification.html");

def projectsoftdetails(request):
	return render(request,"otherapps/admin/projectsoftdetails.html");

def allprojectsrequests(request):
	return render(request,"otherapps/admin/allprojectsrequests.html");

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/admin/activeprojects.html");
def completedprojects(request):
	return render(request,"otherapps/admin/completedprojects.html");

# new 
def recruitments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/admin/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/admin/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/admin/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/admin/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/admin/allmessages.html");

def reportscollection(request):
	return render(request,"otherapps/admin/reportscollection.html");
def sendreports(request):
	return render(request,"otherapps/admin/sendreports.html");
def sendreportsopen(request,username):
	return render(request,"otherapps/admin/sendreportsopen.html");
def creativeteam(request):
	return render(request,"otherapps/admin/creativeteam.html");


