from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
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
				temp=Employee.objects.get(pk=lock.id)
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
				temp=Employee.objects.get(pk=lock.id)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			value.Developer=locks
	return render(request,"otherapps/hr/completedprojects.html", {'values':values});

def latestreport(request,projectslug):
	return render(request, "otherapps/hr/reportsopen.html", {'projectslug':projectslug}) 

def completedprojectdetails(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	print(values,values.Client,values.Admin)
	ClientFullName=ClientInfo.objects.get(id=values.Client).FullName
	AdminFullName=Employee.objects.get(id=values.Admin).FullName
	return render(request, "otherapps/hr/completedprojectdetails.html", {'values':values, 'projectslug':projectslug, 'ClientFullName':ClientFullName, 'AdminFullName':AdminFullName})

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
	AdminsID=None
	if request.method=="POST":
		values=ProjectInfo.objects.get(pk=request.POST["employeeID"])
		if(request.POST["admin"]):
			values.Admin=AdminsID=request.POST["admin"];
			print(values.Admin,AdminsID)
			values.ReportStatus="Active"
		values.save()
		return redirect('/allprojectsrequests/')
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	ClientFullName=ClientInfo.objects.get(pk=values.Client).FullName
	adminslist=Employee.objects.filter(~Q(CompanyJoiningDate=None), Role='Admin')
	return render(request,"otherapps/hr/projectdetails_proceed.html",{'values':values, 'path':request.path, 'ClientFullName':ClientFullName, 'AdminsID':AdminsID, 'adminslist':adminslist});

def projectdetailsedit(request,projectslug):
	if request.method=="POST":
		prevPATH=request.POST["prevPATH"];
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
		lock.save()
		return redirect(prevPATH)
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	# --------------------------------------------------------------
	# NOTE : below we are getting our previous url...
	# print(request.META.get('HTTP_REFERER'))
	overallURL=request.META['HTTP_REFERER']
	prevPATH=overallURL[21:]  #''.join(overallURL.split('/')[3:])
	print(prevPATH,prevPATH)
	return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'values':values, 'path':request.path, 'prevPATH':prevPATH});


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
		return redirect('/listof/newjoinees/')
	values = Employee.objects.get(Username=username)
	print(values)
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
		values.EmploymentID = generateID(),
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
		# return redirect('/trialcenter/'+str(values.id))
		# values=Employee.objects.get(pk=values.id)
		return render(request,"otherapps/hr/recruitments.html",{'values':values});
	return render(request,"otherapps/hr/recruitments.html");

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
		return redirect('/listof/promotions/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/promotions.html",{'values':values});

def increments(request,username):
	if request.method=="POST":
		PIDsSubmission(request)
		return redirect('/listof/increments/')
	values = Employee.objects.get(Username=username)
	return render(request,"otherapps/hr/increments.html",{'values':values});

def decrements(request,username):
	if request.method=="POST":
		PIDsSubmission(request)
		return redirect('/listof/decrements/')
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
# def allsuggestions(request):
# 	return render(request,"otherapps/hr/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/hr/allmessages.html");



def trialcenter(request,key):
	values=Employee.objects.get(pk=int(key))
	# return render(request,"otherapps/hr/recruitments.html",{'values':values});
	return render(request,"otherapps/hr/trialcenter.html",{'values':values});
















