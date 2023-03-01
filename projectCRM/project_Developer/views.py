from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
from project_Admin.models import ReportsOrMessages,AllMessages,AllSuggestions
from project_ProjectManager.models import AllTasks
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
	ProjectID=int(projectslug.split('-')[-1])
	# here is we getting our last date on which project manager giving a response, because only then reports approved...
	lastRecord = ReportsOrMessages.objects.filter(ProjectID=ProjectID, SenderRole="Project Manager").last()
	SelectedDate = lastRecord.SendingDateTime if(lastRecord) else datetime.date.today()
	values=list()
	if(lastRecord):  # if we getting lastRecord, then its running, else no need to go with this IF...
		values=ReportsOrMessages.objects.filter(ProjectID=ProjectID, SendingDateTime__date=SelectedDate)
	holdingDict = setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
	holdingDict |= {'projectslug':projectslug}
	return render(request, "otherapps/developer/reportsopen.html", holdingDict) 


def allprojectsrequests(request):  #✓
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		# actually if this persongiving any single report or suggestion on that project then come true, and for true we not pick this to show...
		passing = len(AllSuggestions.objects.filter(ProjectID=getting.id, SenderID=DeveloperMain, SenderRole="Developer")) \
				| len(ReportsOrMessages.objects.filter(ProjectID=getting.id, SenderID=DeveloperMain, SenderRole="Developer"))
		if(getting.ReportStatus=="Active" and not passing): 
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
	passing=len(AllSuggestions.objects.filter(ProjectID=key, SenderID=DeveloperMain, SenderRole="Developer"))
	comingFrom = ('Active' if(passing) else 'New')
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
		# actually if this persongiving any single report or suggestion on that project then come true, and for true we not pick this to show...
		passing = len(AllSuggestions.objects.filter(ProjectID=getting.id, SenderID=DeveloperMain, SenderRole="Developer")) \
				| len(ReportsOrMessages.objects.filter(ProjectID=getting.id, SenderID=DeveloperMain, SenderRole="Developer"))
		if(getting.ReportStatus=="Active" and passing):	
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


# this function helps just below function, where we needed a dataset for a need...
def setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values,SenderID=None):
	holdingDict=dict()
	# getting=ProjectInfo.objects.get(pk=ProjectID).ProjectSlug.split('-')
	detailsSet={'Date':SelectedDate, 
			'ProjectUsername':''.join(ProjectInfo.objects.get(pk=ProjectID).ProjectSlug.split('-'))}
	templist=list()
	temp=ProjectInfo.objects.get(pk=ProjectID).ProjectManager
	templist.append(Employee.objects.get(pk=temp))
	temps=DeveloperBox.objects.filter(ProjectInfosID=ProjectID)
	for temp in temps:
		templist.append(Employee.objects.get(pk=temp.DeveloperID))
	detailsSet['PMnDevs']=templist   # third assignment
	for value in values:
		if(value.SenderID==SenderID):
			detailsSet['textareaReadonly']=True
		value.SenderID=Employee.objects.get(pk=value.SenderID)
	holdingDict={'detailsSet':detailsSet, 'values':values}
	return holdingDict

def reportscollection(request):  #✓
	QueryDataSets=list()
	SelectedDataSets=dict()
	if request.method=="POST":   
		SelectedDate=request.POST["selecteddate"] if(request.POST["selecteddate"]) else None
		ProjectID=int(request.POST["projectid"]) if(request.POST["projectid"]) else None
		SelectedDataSets={'SelectedDate':SelectedDate, 'ProjectID':ProjectID}
		if(ProjectID):   # here is take ProjectID's ProjectName, but we take it if it existing there!!!
			SelectedDataSets['ProjectName']=ProjectInfo.objects.get(pk=ProjectID).ProjectName
		if(SelectedDate):  # first here is we convert this date to a original format of date, but if it is exist!!!
			SelectedDate=datetime.datetime.strptime(SelectedDate, '%Y-%m-%dT%H:%M')
		if(SelectedDate and ProjectID):
			values=ReportsOrMessages.objects.filter(ProjectID=ProjectID, SendingDateTime__date=SelectedDate)
			if(values):   #
				holdingDict = setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
				QueryDataSets.append(holdingDict)
		elif(SelectedDate):
			values=ReportsOrMessages.objects.filter(SendingDateTime__date=SelectedDate)
			collections = dict()
			for value in values:
				getting = collections.get(value.ProjectID,[]) + [value]
				collections[value.ProjectID]=getting
			keys=collections.keys()
			keys=list(keys)
			keys.sort()
			valuesDataSets=[ collections[key] for key in keys ]
			for values in valuesDataSets:
				ProjectID=values[0].ProjectID
				holdingDict=setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
				QueryDataSets.append(holdingDict)
		elif(ProjectID):
			values=ReportsOrMessages.objects.filter(ProjectID=ProjectID)
			collections = dict()
			for value in values:
				getting = collections.get(str(value.SendingDateTime)[:10],[]) + [value]
				collections[str(value.SendingDateTime)[:10]]=getting
			keys=collections.keys()
			keys=list(keys)
			keys.sort()
			valuesDataSets=[ collections[key] for key in keys ]
			for values in valuesDataSets:
				SelectedDate=values[0].SendingDateTime
				holdingDict=setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
				QueryDataSets.append(holdingDict)
		else:  #
			pass
	querysets=DeveloperBox.objects.filter(DeveloperID=DeveloperMain)
	values=list()
	for queryset in querysets:
		getting = ProjectInfo.objects.get(pk=queryset.ProjectInfosID_id)
		if(getting.ReportStatus=="Active"):
			values.append(getting)
	return render(request,"otherapps/developer/reportscollection.html", {'values':values, 'selected':SelectedDataSets, 'QueryDataSets':QueryDataSets});




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
	ProjectID=int(projectslug.split('-')[-1])
	SelectedDate=datetime.date.today()   #datetime.date(2023, 2, 18) // for trial
	values=ReportsOrMessages.objects.filter(ProjectID=ProjectID, SendingDateTime__date=SelectedDate)
	holdingDict=setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values,DeveloperMain)
	holdingDict |= {'projectslug':projectslug}
	return render(request,"otherapps/developer/sendreportsopen.html", holdingDict);



def assignedtasks(request):
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
	return render(request,"otherapps/developer/assignedtasks.html", {'values':values});


def assignedtasksopen(request,projectslug):
	ProjectID=int(projectslug.split('-')[-1])
	if request.method=="POST":   
		if(request.POST["githublink"]):
			lock=AllTasks.objects.get(pk=request.POST["thistasksID"])
			lock.GitHubLink=request.POST["githublink"]
			lock.TaskStatus=True
			lock.save()
		return redirect(request.path)
	# values=AllTasks.objects.filter(ReceiverID=DeveloperMain, TaskStatus=False)
	values=AllTasks.objects.filter(ProjectID=ProjectID,ReceiverID=DeveloperMain,TaskStatus=False)
	# getting=ProjectInfo.objects.get(pk=ProjectID).ProjectSlug.split('-')
	detailsSet={'ProjectUsername':''.join(ProjectInfo.objects.get(pk=ProjectID).ProjectSlug.split('-'))}
	templist=list()
	temp=ProjectInfo.objects.get(pk=ProjectID).ProjectManager
	templist.append(Employee.objects.get(pk=temp))
	temps=DeveloperBox.objects.filter(ProjectInfosID=ProjectID)
	for temp in temps:
		templist.append(Employee.objects.get(pk=temp.DeveloperID))
	detailsSet['PMnDevs']=templist   # third assignment
	for value in values:
		value.ProjectID=ProjectInfo.objects.get(pk=value.ProjectID)
	holdingDict={'detailsSet':detailsSet, 'values':values, 'projectslug':projectslug}
	return render(request,"otherapps/developer/assignedtasksopen.html", holdingDict);


def allassignedtasks(request):
	if request.method=="POST":   
		if(request.POST["githublink"]):
			lock=AllTasks.objects.get(pk=request.POST["thistasksID"])
			lock.GitHubLink=request.POST["githublink"]
			lock.TaskStatus=True
			lock.save()
		return redirect(request.path)
	values=AllTasks.objects.filter(ReceiverID=DeveloperMain,TaskStatus=False)
	for value in values:
		value.ProjectID=ProjectInfo.objects.get(pk=value.ProjectID)
	return render(request,"otherapps/developer/allassignedtasks.html", {'values':values});










