from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
from project_Admin.models import ReportsOrMessages,AllMessages,AllSuggestions
# from django.utils import timezone
from django.db.models import Q
import datetime


DeveloperMain=5


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
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	getting=projectslug.split('-')
	key=int(getting[-1])
	# here is we getting our last date on which project manager giving a response, because only then reports approved...
	lastRecord = ReportsOrMessages.objects.filter(ProjectID=key, SenderRole="Project Manager").last()
	lastrecordsDateTime = lastRecord.SendingDateTime if(lastRecord) else datetime.date.today()
	values=list()
	if(lastRecord):
		values=ReportsOrMessages.objects.filter(ProjectID=key, SendingDateTime__date=lastrecordsDateTime)
		for value in values:
			value.SenderID=Employee.objects.get(pk=value.SenderID)
	detailsSet={'Date':lastrecordsDateTime, 'ProjectUsername':''.join(getting[:-1])}
	templist=list()
	temp=ProjectInfo.objects.get(pk=key).ProjectManager
	templist.append(Employee.objects.get(pk=temp))
	temps=DeveloperBox.objects.filter(ProjectInfosID=key)
	for temp in temps:
		templist.append(Employee.objects.get(pk=temp.DeveloperID))
	detailsSet['PMnDevs']=templist   # third assignment 
	return render(request, "otherapps/developer/reportsopen.html", {'projectslug':projectslug, 'values':values, 'detailsSet':detailsSet}) 


def allprojectsrequests(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus=="Active"):	
			getting.Client=ClientInfo.objects.get(pk=getting.Client).FullName
			values.append(getting)
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
	if request.method=="POST":   
		values=AllSuggestions()
		values.ProjectID = key
		values.SenderID = DeveloperMain
		values.SenderRole = Employee.objects.get(pk=DeveloperMain).Role
		values.ContentData = request.POST["contentdata"]
		values.save()
		return redirect(request.path)
	values=ProjectInfo.objects.get(pk=key)
	values.Client=ClientFullName=ClientInfo.objects.get(id=values.Client).FullName
	values.Admin=Employee.objects.get(id=values.Admin).FullName
	overallURL=(request.META['HTTP_REFERER'])
	comingFrom = ('Active' if('active' in overallURL) else 'New')
	myAllSuggestions=AllSuggestions.objects.filter(ProjectID=key)
	for temp in myAllSuggestions:
		if(temp.SenderID):  # if sender is not HR, because its SenderID have None, so its official ERROR...
			temp.SenderID = ClientInfo.objects.get(pk=temp.SenderID) if(temp.SenderRole=="Client") else Employee.objects.get(pk=temp.SenderID)
		else:
			temp.SenderID = {'FullName': 'ShivaShu'}
	temp=ProjectInfo.objects.get(pk=key).ProjectManager
	detailsSet = [Employee.objects.get(pk=temp)] if(temp) else []
	temps=DeveloperBox.objects.filter(ProjectInfosID=key)
	for temp in temps:
		detailsSet.append(Employee.objects.get(pk=temp.DeveloperID))
	profileData=Employee.objects.get(pk=DeveloperMain)
	return render(request,"otherapps/developer/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom, 'profileData':profileData, 'myAllSuggestions':myAllSuggestions, 'detailsSet':detailsSet});


# currently we refer both urls to a duplicate page
def activeprojects(request):  #✓
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
	return render(request,"otherapps/developer/activeprojects.html", {'values':values});


def completedprojects(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
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
	return render(request,"otherapps/developer/sendreports.html", {'values':values});

def sendreportsopen(request,projectslug=None):  #✓
	if request.method=="POST":   
		# get key from url's slug ---> 'shivam-shukla-77' to '77'...
		key=int(projectslug.split('-')[-1])
		values=ReportsOrMessages()
		values.ProjectID=key
		values.WhatIsIt=request.POST["whatisit"]
		values.SenderID=DeveloperMain
		values.SenderRole="Developer"  #projectmanager/developer
		values.ContentData=request.POST["contentdata"]
		values.save()
		return redirect(request.path)
	getting=projectslug.split('-')
	key=int(getting[-1])
	detailsSet={'Date':datetime.date.today(), 'ProjectUsername':''.join(getting[:-1])}
	templist=list()
	temp=ProjectInfo.objects.get(pk=key).ProjectManager
	templist.append(Employee.objects.get(pk=temp))
	temps=DeveloperBox.objects.filter(ProjectInfosID=key)
	for temp in temps:
		templist.append(Employee.objects.get(pk=temp.DeveloperID))
	detailsSet['PMnDevs']=templist   # third assignment
	values=ReportsOrMessages.objects.filter(ProjectID=key, SendingDateTime__date=datetime.date.today())
	for value in values:
		if(value.SenderID==DeveloperMain):
			detailsSet['textareaReadonly']=True
		value.SenderID=Employee.objects.get(pk=value.SenderID)
	return render(request,"otherapps/developer/sendreportsopen.html", {'projectslug':projectslug, 'values':values, 'detailsSet':detailsSet});









