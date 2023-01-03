from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return render(request,"index.html");
'''
def index(request):
	return render(request,"client/clientdetails.html");
	return HttpResponse("This is <b>client</b> page!!!");

def clientdetails(request):
	return render(request,"client/clientdetails.html");





