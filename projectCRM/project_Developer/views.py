from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return HttpResponse("This is <b>developer</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/developer/index.html");

def allprojects(request):
	return render(request,"otherapps/developer/allprojects.html");



