from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
from project_Admin.models import ReportsOrMessages,AllMessages,AllSuggestions
# from django.utils import timezone
from django.db.models import Q
import datetime




'''
def index(request):
	return HttpResponse("This is <b>HR</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/hr/index.html");

def myaccount(request):
	return render(request,"otherapps/hr/myaccount.html");
def mynotification(request):
	return render(request,"otherapps/hr/mynotification.html");
def myconnections(request):
	return render(request,"otherapps/hr/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/hr/mydeactivate.html");


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
	return render(request, "otherapps/hr/reportsopen.html", holdingDict) 


def allprojectsrequests(request):
	# Below we use developer because it is the last thing wheich we insert... otherwise also use ProjectManager=None...
	querysets=ProjectInfo.objects.filter(ReportStatus="Not Received")
	values=list()
	for queryset in querysets:
		queryset.Client=ClientInfo.objects.get(pk=queryset.Client).FullName
		values.append(queryset)
	return render(request,"otherapps/hr/allprojectsrequests.html",{'values':values});

# currently we refer both urls to a duplicate page
def activeprojects(request):
	values=ProjectInfo.objects.filter(ReportStatus="Active")
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
	return render(request,"otherapps/hr/activeprojects.html", {'values':values});

def completedprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Completed") \
				| ProjectInfo.objects.filter(ReportStatus="Withdrawal")
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
	return render(request,"otherapps/hr/completedprojects.html", {'values':values});


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
	ShowEditButton = True if('active' in request.path) else False
	return render(request, "otherapps/hr/completedprojectdetails.html", {'values':values, 'projectslug':projectslug, 'ShowEditButton':ShowEditButton, 
	 'selectedprojectmanager':selectedprojectmanager, 'selecteddeveloperslist':selecteddeveloperslist})

def projectdetails(request):
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
		# hold=ProjectInfo.objects.filter(Client=request.POST["clientID"])
		# return redirect('request,"otherapps/hr/projectdetails.html"');
		return render(request,"otherapps/hr/projectdetails_editorassignnew.html");
	clientID=1
	return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'clientID':clientID}); 
	# return render(request,"otherapps/hr/projectdetails_foractive.html");

def projectdetailsslug(request,projectslug):
	if request.method=="POST":
		values=ProjectInfo.objects.get(pk=request.POST["projectID"])
		if(request.POST["admin"]):
			values.Admin=AdminsID=request.POST["admin"];
			values.ReportStatus="Active"
		values.save()
		return redirect('/hr/allprojectsrequests/')
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	values=ProjectInfo.objects.get(pk=projectslug.split('-')[-1])   
	values.Client=ClientInfo.objects.get(pk=values.Client).FullName
	adminslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Admin')
	return render(request,"otherapps/hr/projectdetails_proceed.html",{'values':values, 'projectslug':projectslug, 'adminslist':adminslist});

def projectdetailsedit(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	if request.method=="POST":
		prevPATH=request.POST["prevPATH"];
		lock=ProjectInfo.objects.get(pk=request.POST["projectID"])
		lock.ProjectName=request.POST["projectname"]
		lock.Admin=request.POST["admin"]
		lock.ProgrammingLanguage=request.POST["programminglanguage"]
		lock.FrontEnd=request.POST["frontend"]
		lock.BackEnd=request.POST["backend"]
		lock.DataBase=request.POST["database"]
		lock.BeginningDate=request.POST["beginningdate"]
		lock.EndingDate=request.POST["endingdate"]
		lock.StartingAmount=request.POST["startingamount"]
		lock.EndingAmount=request.POST["endingamount"]
		# lock.SoftDiscription=request.POST["softdiscription"]  # there is never need comes to rewrite this, its one time!!!
		# lock.HardDiscription=request.POST["harddiscription"]   # and ignore this because only admin can able to fill this!!!
		lock.save()
		if(request.POST["contentdata"]):
			values=AllSuggestions()
			values.ProjectID = key
			# values.SenderID = None   # for HR there is no ID...
			values.SenderRole = 'HR'
			values.ContentData = request.POST["contentdata"]
			values.save()
			return redirect(request.path)
		return redirect(prevPATH)
	values=ProjectInfo.objects.get(pk=key)
	values.Client=ClientInfo.objects.get(id=values.Client).FullName
	# if(values.Admin):
		# values.Admin=Employee.objects.get(id=values.Admin).FullName
	comingFrom = ('Active' if(values.Admin) else 'New')
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
	profileData={'id':None, 'Role':'HR'}
	adminslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Admin')
	orignalURL=(request.META['HTTP_REFERER'])[21:]
	return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'values':values, 'comingFrom':comingFrom, 'profileData':profileData, 'myAllSuggestions':myAllSuggestions, 'detailsSet':detailsSet, 'adminslist':adminslist, 'prevPATH':orignalURL});




# new 
def newjoinees(request,username):
	if request.method=="POST":
		values=Employee.objects.get(pk=request.POST["employeeID"])
		values.EmailId = request.POST["emailid"]
		values.MobileNo = request.POST["mobileno"]
		values.As = request.POST["as"]
		values.Role =request.POST["role"]
		values.Level = request.POST["level"]
		values.OfficeLocation = request.POST["officelocation"]
		values.SittingArea = request.POST["sittingarea"]
		values.Salary = request.POST["salary"]
		values.Contract = request.POST["contract"]
		values.CTC = request.POST["ctc"]		
		# generate the componey joining and living dates...
		mydate = datetime.date.today()
		values.CompanyJoiningDate = mydate
		mydate = mydate.replace(year=mydate.year+2,day=mydate.day-1)
		values.CompanyLeavingDate = mydate
		values.save()
		return redirect('/hr/listof/newjoinees/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/newjoinees.html",{'values':values});

def recruitments(request):
	if request.method=="POST":
		def generateID():
			n=str(Employee.objects.count()+1)
			temp='0'*(4-len(n))+n
			temp='googler'+'emp'+temp
			return temp
		values=Employee()
		values.Username = request.POST["username"]
		values.Password = request.POST["password"]
		values.FirstName = request.POST["firstname"]
		values.LastName = request.POST["lastname"]
		values.FullName = request.POST["firstname"]+' '+request.POST["lastname"]
		values.EmailId = request.POST["emailid"]
		values.MobileNo = request.POST["mobileno"]  # str(int(request.POST["mobileno"])+1),
		values.Address = request.POST["address"]
		values.State = request.POST["state"]
		values.Country = request.POST["country"]
		values.Company = request.POST["company"]
		values.EmploymentID = generateID()   # because it return under tuple
		values.As = request.POST["as"]
		values.Role =request.POST["role"]
		values.Level = request.POST["level"]
		values.OfficeLocation = request.POST["officelocation"]
		values.SittingArea = request.POST["sittingarea"]
		values.JoiningBeginningDate = request.POST["joiningbeginningdate"]
		values.JoiningEndingDate = request.POST["joiningendingdate"]
		values.Salary = request.POST["salary"]
		values.Contract = request.POST["contract"]
		values.CTC = request.POST["ctc"]
		if("upload" in request.FILES):
			values.ProfilePick = request.FILES["upload"]
		values.save()
		# return redirect('/hr/trialcenter/'+str(values.id))
		# values=Employee.objects.get(pk=values.id)
		return render(request,"otherapps/hr/recruitments.html",{'values':values});
	values=Employee.objects.get(pk=1)
	return render(request,"otherapps/hr/recruitments.html",{'values':values});

def PIDsSubmission(request):
	values=Employee.objects.get(pk=request.POST["employeeID"])
	if("newofficelocation" in request.POST and request.POST["newofficelocation"]):
		values.OfficeLocation=request.POST["newofficelocation"]
	if("newsittingarea" in request.POST and request.POST["newsittingarea"]):
		values.SittingArea=request.POST["newsittingarea"]
	if(request.POST["newas"]):
		values.As=request.POST["newas"]
	if(request.POST["newrole"]):
		values.Role=request.POST["newrole"]
	if(request.POST["newlevel"]):
		values.Level=request.POST["newlevel"]
	if(request.POST["newsalary"]):
		values.Salary+=int(request.POST["newsalary"])
	if("newcontract" in request.POST and request.POST["newcontract"]):
		# below we control two things, because if contract extend, then CompanyLeavingDate is also extend!!!
		temp = int(request.POST["newcontract"])
		mydate = values.CompanyLeavingDate
		values.CompanyLeavingDate = mydate.replace(year=mydate.year+temp)
		values.Contract+=int(request.POST["newcontract"])
	if(request.POST["newctc"]):
		values.CTC=request.POST["newctc"]
	values.save()
	return None

def promotions(request,username):
	if request.method=="POST":
		PIDsSubmission(request)
		return redirect('/hr/listof/promotions/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/promotions.html",{'values':values});

def increments(request,username):
	if request.method=="POST":
		PIDsSubmission(request)
		return redirect('/hr/listof/increments/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/increments.html",{'values':values});

def decrements(request,username):
	if request.method=="POST":
		PIDsSubmission(request)
		return redirect('/hr/listof/decrements/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/decrements.html",{'values':values});

def listof(request,target):
	pickfromtarget={'newjoinees':'Join Now','promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	if(target=='newjoinees'):
		values=Employee.objects.filter(CompanyJoiningDate=None)
	elif(target=='promotions'):
		values=Employee.objects.filter(~Q(CompanyJoiningDate=None, ))
	elif(target=='increments'):
		values=Employee.objects.filter(~Q(CompanyJoiningDate=None, ))
	elif(target=='decrements'):
		values=Employee.objects.filter(~Q(CompanyJoiningDate=None))		
	return render(request,"otherapps/hr/listof.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target], "values":values});
	# return render(request,"otherapps/hr/listof.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target], "values":values});


def alldiscussions(request):
	return render(request,"otherapps/hr/alldiscussions.html");
def allmessages(request):
	return render(request,"otherapps/hr/allmessages.html");





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
	values=ProjectInfo.objects.filter(HR=None,ReportStatus="Active")
	return render(request,"otherapps/hr/reportscollection.html", {'values':values, 'selected':SelectedDataSets, 'QueryDataSets':QueryDataSets});

















