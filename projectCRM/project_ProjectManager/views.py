from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
from project_Admin.models import ReportsOrMessages,AllMessages,AllSuggestions
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
	return render(request, "otherapps/projectmanager/reportsopen.html", holdingDict) 


def allprojectsrequests(request):  #✓
	# Below we use developer because it is the last thing wheich we insert... otherwise also use ProjectManager=None...
	querysets=ProjectInfo.objects.filter(ReportStatus="Active", ProjectManager=ProjectManagerMain)
	values=list()
	for queryset in querysets:
		# print(queryset.id, ProjectManagerMain, "Project Manager", end='  ')
		passing = len(AllSuggestions.objects.filter(ProjectID=queryset.id, SenderID=ProjectManagerMain, SenderRole="Project Manager"))
		# print(passing,end=" ")
		if(not passing):
			queryset.Client=ClientInfo.objects.get(pk=queryset.Client).FullName
			values.append(queryset)
		# print("  Done")
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
	if request.method=="POST":   
		values=AllSuggestions()
		values.ProjectID = key
		values.SenderID = ProjectManagerMain
		values.SenderRole = Employee.objects.get(pk=ProjectManagerMain).Role
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
		if(temp.SenderID): # if sender is not HR, because its SenderID have None, so its official ERROR...
			temp.SenderID = ClientInfo.objects.get(pk=temp.SenderID) if(temp.SenderRole=="Client") else Employee.objects.get(pk=temp.SenderID)
		else:
			temp.SenderID = {'FullName': 'ShivaShu'}
	temp=ProjectInfo.objects.get(pk=key).ProjectManager
	detailsSet = [Employee.objects.get(pk=temp)] if(temp) else []
	temps=DeveloperBox.objects.filter(ProjectInfosID=key)
	for temp in temps:
		detailsSet.append(Employee.objects.get(pk=temp.DeveloperID))
	profileData=Employee.objects.get(pk=ProjectManagerMain)
	return render(request,"otherapps/projectmanager/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom, 'profileData':profileData, 'myAllSuggestions':myAllSuggestions, 'detailsSet':detailsSet});


# currently we refer both urls to a duplicate page
def activeprojects(request):  #✓
	# querysets=ProjectInfo.objects.get(pk=ProjectManagerMain)
	querysets=ProjectInfo.objects.filter(ReportStatus="Active", ProjectManager=ProjectManagerMain)
	values=list()
	for queryset in querysets:
		passing = len(AllSuggestions.objects.filter(ProjectID=queryset.id, SenderID=ProjectManagerMain, SenderRole="Project Manager"))
		if(passing):
			queryset.Client=ClientInfo.objects.get(pk=queryset.Client)
			queryset.Admin=Employee.objects.get(pk=queryset.Admin)
			queryset.ProjectManager=Employee.objects.get(pk=queryset.ProjectManager)
			if(queryset.Developer):
				locks=DeveloperBox.objects.filter(ProjectInfosID=queryset.id)
				for lock in locks:
					temp=Employee.objects.get(pk=lock.DeveloperID)
					lock.FullName=temp.FullName
					lock.ProfilePick=temp.ProfilePick
				queryset.Developer=locks
			values.append(queryset)
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
		print(SelectedDate,ProjectID)
		SelectedDataSets={'SelectedDate':SelectedDate, 'ProjectID':ProjectID}
		if(ProjectID):   # here is take ProjectID's ProjectName, but we take it if it existing there!!!
			SelectedDataSets['ProjectName']=ProjectInfo.objects.get(pk=ProjectID).ProjectName
		if(SelectedDate):  # first here is we convert this date to a original format of date, but if it is exist!!!
			SelectedDate=datetime.datetime.strptime(SelectedDate, '%Y-%m-%dT%H:%M')
		print(SelectedDate,ProjectID) 
		print(">>>>> 1")
		if(SelectedDate and ProjectID):
			print(">>>>> 2")
			values=ReportsOrMessages.objects.filter(ProjectID=ProjectID, SendingDateTime__date=SelectedDate)
			if(values):   #
				holdingDict = setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
				QueryDataSets.append(holdingDict)
		elif(SelectedDate):
			print(">>>>> 3")
			values=ReportsOrMessages.objects.filter(SendingDateTime__date=SelectedDate)
			collections = dict()
			for value in values:
				getting = collections.get(value.ProjectID,[]) + [value]
				collections[value.ProjectID]=getting
			keys=collections.keys()
			keys=list(keys)
			keys.sort()
			valuesDataSets=[ collections[key] for key in keys ]
			print(valuesDataSets)
			for values in valuesDataSets:
				ProjectID=values[0].ProjectID
				holdingDict=setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values)
				QueryDataSets.append(holdingDict)
		elif(ProjectID):
			print(">>>>> 4")
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
			print(">>>>> 5")
			pass
		print(">>>>> 6")
	values=ProjectInfo.objects.filter(ProjectManager=ProjectManagerMain,ReportStatus="Active")
	print(values)
	return render(request,"otherapps/projectmanager/reportscollection.html", {'values':values, 'selected':SelectedDataSets, 'QueryDataSets':QueryDataSets});

	
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


def sendreportsopen(request,projectslug=None):  #✓
	if request.method=="POST":
		# get key from url's slug ---> 'shivam-shukla-77' to '77'...
		key=int(projectslug.split('-')[-1])
		values=ReportsOrMessages()
		values.ProjectID=key
		values.WhatIsIt=request.POST["whatisit"]
		values.SenderID=ProjectManagerMain
		values.SenderRole="Project Manager"  # Project Manager / Developer
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
		if(value.SenderID==ProjectManagerMain):
			detailsSet['textareaReadonly']=True
		value.SenderID=Employee.objects.get(pk=value.SenderID)
	return render(request,"otherapps/projectmanager/sendreportsopen.html", {'projectslug':projectslug, 'values':values, 'detailsSet':detailsSet});

def sendreportsopen(request,projectslug=None):  #✓
	if request.method=="POST":
		# get key from url's slug ---> 'shivam-shukla-77' to '77'...
		key=int(projectslug.split('-')[-1])
		values=ReportsOrMessages()
		values.ProjectID=key
		values.WhatIsIt=request.POST["whatisit"]
		values.SenderID=ProjectManagerMain
		values.SenderRole="Project Manager"  # Project Manager / Developer
		values.ContentData=request.POST["contentdata"]
		values.save()
		return redirect(request.path)
	ProjectID=int(projectslug.split('-')[-1])
	SelectedDate=datetime.date.today()   #datetime.date(2023, 2, 18) // for trial
	values=ReportsOrMessages.objects.filter(ProjectID=ProjectID, SendingDateTime__date=SelectedDate)
	holdingDict=setupaccordingtoProjectIDnSelectedDate(ProjectID,SelectedDate,values,ProjectManagerMain)
	holdingDict |= {'projectslug':projectslug}
	print(holdingDict)
	return render(request,"otherapps/projectmanager/sendreportsopen.html", holdingDict);










