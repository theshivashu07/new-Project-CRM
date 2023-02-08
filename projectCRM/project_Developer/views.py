from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>Developer</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/developer/index.html");

def myaccount(request):
	return render(request,"otherapps/developer/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/developer/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/developer/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/developer/mynotification.html");

def projectdetails(request):
	return render(request,"otherapps/developer/projectdetails.html");

def allprojectsrequests(request):
	return render(request,"otherapps/developer/allprojectsrequests.html");

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/developer/activeprojects.html");
def completedprojects(request):
	return render(request,"otherapps/developer/completedprojects.html");

# new 
def recruitments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/developer/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/developer/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/developer/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/developer/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/developer/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/developer/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/developer/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/developer/allmessages.html");

def reportscollection(request):
	return render(request,"otherapps/developer/reportscollection.html");
def sendreports(request):
	return render(request,"otherapps/developer/sendreports.html");
# def creativeteam(request):
# 	return render(request,"otherapps/developer/creativeteam.html");









