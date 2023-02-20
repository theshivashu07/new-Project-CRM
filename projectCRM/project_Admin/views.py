from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
from .models import ReportsOrMessages,AllMessages,AllSuggestions
# from django.utils import timezone
from django.db.models import Q
import datetime


AdminMain=1




'''
def index(request):
	return HttpResponse("This is <b>Admin</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/admin/index.html");

def myaccount(request):
	return render(request,"otherapps/admin/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/admin/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/admin/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/admin/mynotification.html");

def projectdetails(request):
	return render(request,"otherapps/admin/projectdetails.html");

def latestreport(request,projectslug):
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
	return render(request, "otherapps/admin/reportsopen.html", {'projectslug':projectslug, 'values':values, 'detailsSet':detailsSet}) 

def completedprojectdetails(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	values.Client=ClientInfo.objects.get(id=values.Client).FullName
	values.Admin=Employee.objects.get(id=values.Admin).FullName
	developerslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Developer')
	selectedprojectmanager=selecteddeveloperslist=0
	if(values.ProjectManager):
		selectedprojectmanager=Employee.objects.get(pk=values.ProjectManager)
	if(values.Developer):
		selecteddeveloperslist=list()
		for developer in developerslist:
			temp=DeveloperBox.objects.filter(ProjectInfosID=values,DeveloperID=developer.id)
			if(temp):
				selecteddeveloperslist.append(developer)
	return render(request, "otherapps/admin/completedprojectdetails.html", {'values':values, 'projectslug':projectslug, 'selectedprojectmanager':selectedprojectmanager, 'selecteddeveloperslist':selecteddeveloperslist})

def allprojectsrequests(request):
	# We only take it, when both are empty...
	querysets=ProjectInfo.objects.filter(ReportStatus="Active", Admin=AdminMain, ProjectManager=None, Developer=None)
	values=list()
	for queryset in querysets:
		queryset.Client=ClientInfo.objects.get(pk=queryset.Client).FullName
		values.append(queryset)
	return render(request,"otherapps/admin/allprojectsrequests.html",{'values':values});

def projectdetailsslug(request,projectslug):
	if request.method=="POST":
		lock=ProjectInfo.objects.get(pk=request.POST["projectID"])
		if(request.POST["projectmanager"] not in ["","None"]): 
			lock.ProjectManager=request.POST["projectmanager"];
			lock.save()
		if(request.POST["developer"]):
			# what if in initial we have no developer, None, so must to put 1 at that time...
			lock.Developer = lock.Developer+1 if(lock.Developer) else 1
			lock.save()
			values=DeveloperBox()
			values.ProjectInfosID=lock
			values.DeveloperID=request.POST["developer"];
			values.save()
		overallURL=(request.META['HTTP_REFERER'])
		orignalURL=overallURL[21:]
		return redirect(orignalURL)
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	temp=DeveloperBox.objects.filter(ProjectInfosID_id=key)
	values.Client=ClientInfo.objects.get(pk=values.Client).FullName
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
	return render(request,"otherapps/admin/projectdetails.html", {'values':values, 'projectslug':projectslug,
		'projectmanagerslist':projectmanagerslist, 'developerslist':developerslist, 'selectedprojectmanager':selectedprojectmanager , 'selecteddeveloperslist':selecteddeveloperslist});

def projectdetailsremoveteammember(request,projectslug):
	temp=projectslug.split('-')
	if(len(temp)==2):   # it's for developer
		lock=ProjectInfo.objects.get(pk=temp[0])
		# if the last developer you removed, so must that you set None there...
		lock.Developer = lock.Developer-1 if(lock.Developer-1) else None
		lock.save()
		lock=DeveloperBox.objects.get(ProjectInfosID=temp[0],DeveloperID=temp[1])
		lock.delete() 
	else:   # it's for project manager
		lock=ProjectInfo.objects.get(pk=temp[0])
		lock.ProjectManager=None
		lock.save()
	overallURL=(request.META['HTTP_REFERER'])
	orignalURL=overallURL[21:]
	return redirect(orignalURL)


def projectdetailsedit(request,projectslug):  #✓
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	if request.method=="POST":   
		values=AllSuggestions()
		values.ProjectID = key
		values.SenderID = AdminMain
		values.SenderRole = Employee.objects.get(pk=AdminMain).Role
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
	temp=ProjectInfo.objects.get(pk=key).ProjectManager
	detailsSet = [Employee.objects.get(pk=temp)] if(temp) else []
	temps=DeveloperBox.objects.filter(ProjectInfosID=key)
	for temp in temps:
		detailsSet.append(Employee.objects.get(pk=temp.DeveloperID))
	profileData=Employee.objects.get(pk=AdminMain)
	return render(request,"otherapps/admin/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom, 'profileData':profileData, 'myAllSuggestions':myAllSuggestions, 'detailsSet':detailsSet});


# currently we refer both urls to a duplicate page
def activeprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(~Q(ProjectManager=None) | ~Q(Developer=None),ReportStatus="Active", Admin=AdminMain)
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
	return render(request,"otherapps/admin/activeprojects.html", {'values':values});

def completedprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Completed", Admin=AdminMain) \
				| ProjectInfo.objects.filter(ReportStatus="Withdrawal", Admin=AdminMain)
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
	return render(request,"otherapps/admin/completedprojects.html", {'values':values});

# new 
def recruitments(request):
	return render(request,"otherapps/admin/recruitments.html");
def promotions(request):
	return render(request,"otherapps/admin/promotions.html");
def increments(request):
	return render(request,"otherapps/admin/increments.html");
def decrements(request):
	return render(request,"otherapps/admin/decrements.html");
def pick(request,target):
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/admin/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/admin/alldiscussions.html");
# def allsuggestions(request):
# 	return render(request,"otherapps/admin/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/admin/allmessages.html");

def reportscollection(request):
	return render(request,"otherapps/admin/reportscollection.html");
def sendreports(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(~Q(ProjectManager=None) & ~Q(Developer=None), ReportStatus="Active", Admin=AdminMain)
	for value in values:
		value.Client=ClientInfo.objects.get(pk=value.Client)
		value.Admin=Employee.objects.get(pk=value.Admin)
		value.ProjectManager=Employee.objects.get(pk=value.ProjectManager)
		locks=DeveloperBox.objects.filter(ProjectInfosID=value.id)
		for lock in locks:
			temp=Employee.objects.get(pk=lock.DeveloperID)
			lock.FullName=temp.FullName
			lock.ProfilePick=temp.ProfilePick
		value.Developer=locks
	return render(request,"otherapps/admin/sendreports.html", {'values':values});
def sendreportsopen(request,projectslug):
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
	return render(request,"otherapps/admin/sendreportsopen.html", {'projectslug':projectslug, 'values':values, 'detailsSet':detailsSet});
# def creativeteam(request):
# 	return render(request,"otherapps/admin/creativeteam.html");



