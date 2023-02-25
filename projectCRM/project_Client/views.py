from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ClientInfo,ProjectInfo,DeveloperBox
from project_HR.models import Employee
from project_Admin.models import ReportsOrMessages,AllMessages,AllSuggestions
# from django.utils import timezone
from django.db.models import Q
import datetime


ClientMain=1



'''
def index(request):
	return HttpResponse("This is <b>client</b> page!!!");
'''

def index(request):
	# reput()  
	return render(request,"otherapps/client/index.html");

def myaccount(request):
	if request.method=="POST":
		values=ClientInfo(
						Username=request.POST["username"],
						Password=request.POST["password"],
						FirstName=request.POST["firstname"],
						LastName=request.POST["lastname"],
						FullName=request.POST["firstname"]+' '+request.POST["lastname"],
						EmailId=request.POST["email"],
						MobileNo=request.POST["mobileno"],
						Organization=request.POST["organization"],
						Language=request.POST["language"],
						Address=request.POST["address"],
						ZipCode=request.POST["zipcode"],
						State=request.POST["state"],
						Country=request.POST["country"],
						ProfilePick=request.FILES["upload"], )
		values.save()
	return render(request,"otherapps/client/myaccount.html");

def myconnections(request):
	return render(request,"otherapps/client/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/client/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/client/mynotification.html");


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
	return render(request, "otherapps/client/reportsopen.html", holdingDict) 


def projectdetails(request):
	values=list()
	if request.method=="POST":
		values=ProjectInfo(
						Client=request.POST["clientID"],
						ProjectName=request.POST["projectname"],
						ProgrammingLanguage=request.POST["programminglanguage"],
						FrontEnd=request.POST["frontend"],
						BackEnd=request.POST["backend"],
						DataBase=request.POST["database"],
						BeginningDate=request.POST["beginningdate"],
						EndingDate=request.POST["endingdate"],
						StartingAmount=request.POST["startingamount"],
						EndingAmount=request.POST["endingamount"],
						SoftDiscription=request.POST["softdiscription"], 
						ReportStatus="Not Received", )
		values.save()
		slug="{}-{}".format(values.ProjectSlug,values.id)  #slug_creation
		return redirect("/client/projectdetails/"+slug)
		# return render(request,"otherapps/client/projectdetails.html", {'value':values});
	return render(request,"otherapps/client/projectdetails.html", {'value':values, 'clientID':ClientMain});


def projectdetailsslug(request,projectslug):
	if request.method=="POST":
		lock=ProjectInfo.objects.get(pk=request.POST["projectID"])
		lock.ProjectName=request.POST["projectname"]
		lock.ProgrammingLanguage=request.POST["programminglanguage"]
		lock.FrontEnd=request.POST["frontend"]
		lock.BackEnd=request.POST["backend"]
		lock.DataBase=request.POST["database"]
		lock.BeginningDate=request.POST["beginningdate"]
		lock.EndingDate=request.POST["endingdate"]
		lock.StartingAmount=request.POST["startingamount"]
		lock.EndingAmount=request.POST["endingamount"]
		lock.SoftDiscription=request.POST["softdiscription"]
		lock.ReportStatus="Not Received"
		lock.save()
		# return render(request,"otherapps/client/projectdetails.html");
		return redirect('/client/allprojectsrequests/')
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	return render(request,"otherapps/client/projectdetails.html",{'values':values, 'projectslug':projectslug, 'path':request.path});

def projectdetailsedit(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	if request.method=="POST":
		lock=ProjectInfo.objects.get(pk=request.POST["projectID"])
		lock.ProjectName=request.POST["projectname"]
		lock.ProgrammingLanguage=request.POST["programminglanguage"]
		lock.FrontEnd=request.POST["frontend"]
		lock.BackEnd=request.POST["backend"]
		lock.DataBase=request.POST["database"]
		lock.BeginningDate=request.POST["beginningdate"]
		lock.EndingDate=request.POST["endingdate"]
		lock.StartingAmount=request.POST["startingamount"]
		lock.EndingAmount=request.POST["endingamount"]
		lock.HardDiscription=request.POST["harddiscription"]
		lock.save()
		if(request.POST["contentdata"]):
			values=AllSuggestions()
			values.ProjectID = key
			values.SenderID = ClientMain
			# values.SenderRole = ClientInfo.objects.get(pk=ClientMain).Role  # not use this because here is not Role field!!!
			values.SenderRole = 'Client'
			values.ContentData = request.POST["contentdata"]
			values.save()
			return redirect(request.path)
		return redirect('/client/projectdetails/active/'+projectslug)
	values=ProjectInfo.objects.get(pk=key)
	# values.Client=ClientInfo.objects.get(id=values.Client).FullName
	values.Admin=Employee.objects.get(id=values.Admin).FullName
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
	# profileData=ClientInfo.objects.get(pk=ClientMain)  # not use this because here is not Role field!!!
	profileData={'id':ClientMain, 'Role':'Client'}
	return render(request,"otherapps/client/projectdetails_editorassignnew.html",{'values':values, 'profileData':profileData, 'projectslug':projectslug, 'myAllSuggestions':myAllSuggestions, 'detailsSet':detailsSet});



def allprojectsrequests(request):
	# values=ProjectInfo.objects.all().values('id')
	values=reversed(ProjectInfo.objects.filter(ReportStatus="Not Received", Client=ClientMain))
	# values=reversed(ProjectInfo.objects.filter(ReportStatus="Not Received", Client=ClientMain)\
					# | ProjectInfo.objects.filter(ReportStatus="Withdrawal", Client=ClientMain))
	return render(request,"otherapps/client/allprojectsrequests.html",{'values':values});

# currently we refer both urls to a duplicate page
def activeprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Active", Client=ClientMain)
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
	return render(request,"otherapps/client/activeprojects.html", {'values':values});

def completedprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Completed", Client=ClientMain) \
				| ProjectInfo.objects.filter(ReportStatus="Withdrawal", Client=ClientMain)
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
	return render(request,"otherapps/client/completedprojects.html", {'values':values});


def completedprojectdetails(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	temp=DeveloperBox.objects.filter(ProjectInfosID_id=key)
	AdminFullName=Employee.objects.get(pk=values.Admin).FullName
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
	return render(request,"otherapps/client/completedprojectdetails.html",{'values':values, 'projectslug':projectslug, 'AdminFullName':AdminFullName, 
		'selecteddeveloperslist':selecteddeveloperslist, 'selectedprojectmanager':selectedprojectmanager});

def alldiscussions(request):
	return render(request,"otherapps/client/alldiscussions.html");
def allmessages(request):
	return render(request,"otherapps/client/allmessages.html");




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
	print('>>>',values)
	for value in values:
		print(value)
		if(value.SenderID==SenderID):
			detailsSet['textareaReadonly']=True
		value.SenderID=Employee.objects.get(pk=value.SenderID)
	print('>>',values)
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
	values=ProjectInfo.objects.filter(HR=None,ReportStatus="Active")
	print(values)
	return render(request,"otherapps/client/reportscollection.html", {'values':values, 'selected':SelectedDataSets, 'QueryDataSets':QueryDataSets});




