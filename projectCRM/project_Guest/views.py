from django.shortcuts import render,redirect
from django.http import HttpResponse



'''
def index(request):
	return HttpResponse("This is <b>guest</b> page!!!");
'''
def index(request):
	return render(request,"guest/index.html");

def workprocess(request):
	return render(request,"guest/workprocess.html");

def aboutus(request):
	return render(request,"guest/aboutus.html");

def contactus(request):
	return render(request,"guest/contactus.html");

def loginMethod(request):
	# here split path... "/projectmanager/login/" to ['projectmanager', 'login']...
	urlsAtHere= request.path[1:-1].split('/')
	fromwhere=urlsAtHere[0]
	return render(request,"guest/login.html",{"fromwhere":fromwhere});

def visit(request):
	return HttpResponse("Which app you want to test <b>provide its link there</b>!!!");
	#return redirect("/developer/");




