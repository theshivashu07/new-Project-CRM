from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
# from django.utils import timezone
from django.db.models import Q
import datetime


DeveloperMain=5
ProjectManagerMain=15


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


def latestreport(request,projectslug):  #✓
	return render(request, "otherapps/developer/reportsopen.html", {'projectslug':projectslug}) 


def allprojectsrequests(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	print(querysets)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus=="Active"):	
			getting.Client=ClientInfo.objects.get(pk=getting.Client).FullName
			values.append(getting)
	print(values)
	return render(request,"otherapps/developer/allprojectsrequests.html",{'values':values});


def projectdetailsslug(request,projectslug):  #✓
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	temp=DeveloperBox.objects.filter(ProjectInfosID_id=key)
	ClientFullName=ClientInfo.objects.get(pk=values.Client).FullName
	projectmanagerslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Project Manager')
	developerslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Developer')
	selectedprojectmanager=selecteddeveloperslist=0
	if(values.ProjectManager):
		selectedprojectmanager=Employee.objects.get(pk=values.ProjectManager)
	if(values.Developer):
		selecteddeveloperslist=list()
		developers,developerslist=developerslist,list()
		for devdataset in developers:
			temp=DeveloperBox.objects.filter(ProjectInfosID=values,DeveloperID=devdataset.id)
			if(temp):
				selecteddeveloperslist.append(devdataset)
			else:
				developerslist.append(devdataset)
	return render(request,"otherapps/developer/projectdetails.html", {'values':values, 'ClientFullName':ClientFullName,  'projectslug':projectslug,
		'projectmanagerslist':projectmanagerslist, 'developerslist':developerslist, 'selectedprojectmanager':selectedprojectmanager , 'selecteddeveloperslist':selecteddeveloperslist});


def projectdetailsedit(request,projectslug):  #✓
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	# ClientFullName=ClientInfo.objects.get(pk=values.Client).FullName
	values.Client=ClientFullName=ClientInfo.objects.get(id=values.Client).FullName
	values.Admin=Employee.objects.get(id=values.Admin).FullName
	overallURL=(request.META['HTTP_REFERER'])
	comingFrom = ('Active' if('active' in overallURL) else 'New')
	return render(request,"otherapps/developer/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom});


# currently we refer both urls to a duplicate page
def activeprojects(request):  #✓
	# values=ProjectInfo.objects.get(pk=ProjectManagerMain)
	# values=ProjectInfo.objects.get(pk=ProjectManagerMain)
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus=="Active"):	
			getting.Client=ClientInfo.objects.get(pk=getting.Client)
			getting.Admin=Employee.objects.get(pk=getting.Admin)
			if(getting.ProjectManager):
				getting.ProjectManager=Employee.objects.get(pk=getting.ProjectManager)
			locks=DeveloperBox.objects.filter(ProjectInfosID=getting.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			getting.Developer=locks
			values.append(getting)
	print(values)
	return render(request,"otherapps/developer/activeprojects.html", {'values':values});


def completedprojects(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	print(querysets)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus in ["Completed","Withdrawal"]):
			getting.Client=ClientInfo.objects.get(pk=getting.Client)
			getting.Admin=Employee.objects.get(pk=getting.Admin)
			if(getting.ProjectManager):
				getting.ProjectManager=Employee.objects.get(pk=getting.ProjectManager)
			locks=DeveloperBox.objects.filter(ProjectInfosID=getting.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			getting.Developer=locks
			values.append(getting)
	print(values)
	return render(request,"otherapps/developer/completedprojects.html", {'values':values});


def alldiscussions(request,projectslug=None):  #✓
	return render(request,"otherapps/developer/alldiscussions.html", {'projectslug':projectslug});
def allmessages(request,projectslug=None):  #✓
	return render(request,"otherapps/developer/allmessages.html", {'projectslug':projectslug});


def reportscollection(request):  #✓
	return render(request,"otherapps/developer/reportscollection.html");
def sendreports(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus=="Active" and getting.ProjectManager and getting.Developer):	
			getting.Client=ClientInfo.objects.get(pk=getting.Client)
			getting.Admin=Employee.objects.get(pk=getting.Admin)
			getting.ProjectManager=Employee.objects.get(pk=getting.ProjectManager)
			locks=DeveloperBox.objects.filter(ProjectInfosID=getting.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			getting.Developer=locks
			values.append(getting)
	print(values)
	return render(request,"otherapps/developer/sendreports.html", {'values':values});
def sendreportsopen(request,projectslug=None):  #✓
	return render(request,"otherapps/developer/sendreportsopen.html", {'projectslug':projectslug});



