from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
# from django.utils import timezone
from django.db.models import Q
import datetime


ProjectManagerMain=15




'''
def index(request):
	return HttpResponse("This is <b>Project Manager</b> page!!!");
'''
def index(request):  #✓
	return render(request,"otherapps/projectmanager/index.html");


def myaccount(request):  #✓
	return render(request,"otherapps/projectmanager/myaccount.html");
def myconnections(request):  #✓
	return render(request,"otherapps/projectmanager/myconnections.html");
def mydeactivate(request):  #✓
	return render(request,"otherapps/projectmanager/mydeactivate.html");
def mynotification(request):  #✓
	return render(request,"otherapps/projectmanager/mynotification.html");


def latestreport(request,projectslug):  #✓
	return render(request, "otherapps/projectmanager/reportsopen.html", {'projectslug':projectslug}) 


def allprojectsrequests(request):  #✓
	# Below we use developer because it is the last thing wheich we insert... otherwise also use ProjectManager=None...
	querysets=ProjectInfo.objects.filter(ReportStatus="Active", ProjectManager=ProjectManagerMain)
	values=list()
	for queryset in querysets:
		queryset.Client=ClientInfo.objects.get(pk=queryset.Client).FullName
		values.append(queryset)
	return render(request,"otherapps/projectmanager/allprojectsrequests.html",{'values':values});


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
	return render(request,"otherapps/projectmanager/projectdetails.html", {'values':values, 'ClientFullName':ClientFullName,  'projectslug':projectslug,
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
	return render(request,"otherapps/projectmanager/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom});


# currently we refer both urls to a duplicate page
def activeprojects(request):  #✓
	# values=ProjectInfo.objects.get(pk=ProjectManagerMain)
	values=ProjectInfo.objects.filter(ReportStatus="Active", ProjectManager=ProjectManagerMain)
	for value in values:
		if(value.Client):
			value.Client=ClientInfo.objects.get(pk=value.Client)
		if(value.Admin):
			value.Admin=Employee.objects.get(pk=value.Admin)
		if(value.ProjectManager):
			value.ProjectManager=Employee.objects.get(pk=value.ProjectManager)
		if(value.Developer):
			locks=DeveloperBox.objects.filter(ProjectInfosID=value.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			value.Developer=locks
	return render(request,"otherapps/projectmanager/activeprojects.html", {'values':values});


def completedprojects(request):  #✓
	# values=ProjectInfo.objects.get(pk=ProjectManagerMain)
	values=ProjectInfo.objects.filter(ReportStatus="Completed", ProjectManager=ProjectManagerMain) \
				| ProjectInfo.objects.filter(ReportStatus="Withdrawal", ProjectManager=ProjectManagerMain)
	for value in values:
		if(value.Client):
			value.Client=ClientInfo.objects.get(pk=value.Client)
		if(value.Admin):
			value.Admin=Employee.objects.get(pk=value.Admin)
		if(value.ProjectManager):
			value.ProjectManager=Employee.objects.get(pk=value.ProjectManager)
		if(value.Developer):
			locks=DeveloperBox.objects.filter(ProjectInfosID=value.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			value.Developer=locks
	return render(request,"otherapps/projectmanager/completedprojects.html", {'values':values});


def alldiscussions(request,projectslug=None):  #✓
	return render(request,"otherapps/projectmanager/alldiscussions.html", {'projectslug':projectslug});
def allmessages(request,projectslug=None):  #✓
	return render(request,"otherapps/projectmanager/allmessages.html", {'projectslug':projectslug});


def reportscollection(request):  #✓
	return render(request,"otherapps/projectmanager/reportscollection.html");
def sendreports(request):  #✓
	values=ProjectInfo.objects.filter(~Q(Developer=None), ProjectManager=ProjectManagerMain, ReportStatus="Active")
	for value in values:
		if(value.Client):
			value.Client=ClientInfo.objects.get(pk=value.Client)
		if(value.Admin):
			value.Admin=Employee.objects.get(pk=value.Admin)
		if(value.ProjectManager):
			value.ProjectManager=Employee.objects.get(pk=value.ProjectManager)
		if(value.Developer):
			locks=DeveloperBox.objects.filter(ProjectInfosID=value.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.DeveloperID)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			value.Developer=locks
	return render(request,"otherapps/projectmanager/sendreports.html", {'values':values});
def sendreportsopen(request,projectslug=None):  #✓
	return render(request,"otherapps/projectmanager/sendreportsopen.html", {'projectslug':projectslug});



