from django.shortcuts import render,redirect
from django.http import HttpResponse


'''
def index(request):
	return render(request,"index.html");
'''
def index(request):
	return HttpResponse("This is <b>developer</b> page!!!");




