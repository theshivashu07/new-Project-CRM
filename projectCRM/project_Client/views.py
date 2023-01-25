from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ClientInfo
from .forms import ClientImageInfo


'''
def index(request):
	return HttpResponse("This is <b>client</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/client/index.html");
def clientdetails(request):
	if request.method=="POST":
		print(request)
		print(request.POST["upload"])
		values=ClientInfo(
						FirstName=request.POST["firstname"],
						LastName=request.POST["lastname"],
						FullName=request.POST["firstname"]+' '+request.POST["lastname"],
						EmailId=request.POST["email"],
						MobileNo=request.POST["mobileno"],
						Organization=request.POST["organization"],
						Language=request.POST["language"],
						Address=request.POST["address"],
						ZipCode=request.POST["zipcode"],
						State=request.POST["state"],
						Country=request.POST["country"],
						# JoiningDate=request.POST["joiningdate"],
						# ProfilePick=request.POST["profilepick"], )
						ProfilePick=request.POST["upload"], )
		values.save()
	form = ClientImageInfo()
	return render(request,"otherapps/client/clientdetails.html",{'form':form});
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








