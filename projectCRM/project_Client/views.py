from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>client</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/client/index.html");
def clientdetails(request):
	return render(request,"otherapps/client/clientdetails.html");
def projectsoftdetails(request):
	return render(request,"otherapps/client/projectsoftdetails.html");
def clientconnections(request):
	return render(request,"otherapps/client/clientconnections.html");
def clientdeactivate(request):
	return render(request,"otherapps/client/clientdeactivate.html");
def clientnotification(request):
	return render(request,"otherapps/client/clientnotification.html");
def allprojectsrequests(request):
	return render(request,"otherapps/client/allprojectsrequests.html");

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/client/activeprojects.html");
def reportsopen(request,username):
	return render(request,"otherapps/client/reportsopen.html");
def completedprojects(request):
	return render(request,"otherapps/client/completedprojects.html");
def projectdetails(request,username):
	return render(request,"otherapps/client/projectdetails.html");








