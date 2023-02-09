from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ClientInfo,ProjectInfo,DeveloperBox
from project_HR.models import Employee
# from django.utils import timezone
from django.db.models import Q


ClienMain=1



'''
def index(request):
	return HttpResponse("This is <b>client</b> page!!!");
'''


def reput():
	'''I'm created this function for dual the ProjectInfo's data.'''
	# values=ProjectInfo.objects.values_list('Client','ProjectName','ProgrammingLanguage','FrontEnd','BackEnd','DataBase','BeginningDate','EndingDate','StartingAmount','EndingAmount','SoftDiscription','ReportStatus', )
	values=ProjectInfo.objects.all().values('Client','ProjectName','ProgrammingLanguage','FrontEnd','BackEnd','DataBase','BeginningDate','EndingDate','StartingAmount','EndingAmount','SoftDiscription','ReportStatus', )
	# print('>>>>>',values)
	for value in values:
		lock=ProjectInfo(
						Client=value['Client'],
						ProjectName=value['ProjectName'],
						ProgrammingLanguage=value['ProgrammingLanguage'],
						FrontEnd=value['FrontEnd'],
						BackEnd=value['BackEnd'],
						DataBase=value['DataBase'],
						BeginningDate=value['BeginningDate'],
						EndingDate=value['EndingDate'],
						StartingAmount=value['StartingAmount'],
						EndingAmount=value['EndingAmount'],
						SoftDiscription=value['SoftDiscription'],
						ReportStatus=value['ReportStatus'], )
		lock.save()
	return None




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


def projectdetails(request,projectslug=None):
	values=ClientInfo.objects.get(pk=ClienMain)
	return render(request,"otherapps/client/projectdetails.html",{'values':values, 'clientID':ClienMain});


def projectdetailsslug(request,projectslug):
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
		# return render(request,"otherapps/client/projectdetails.html");
		return redirect('/projectdetails/')
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	return render(request,"otherapps/client/projectdetails.html",{'values':values, 'path':request.path});


def allprojectsrequests(request):
	# values=ProjectInfo.objects.all().values('id')
	values=reversed(ProjectInfo.objects.filter(ReportStatus="Not Received", Client=ClienMain)\
					| ProjectInfo.objects.filter(ReportStatus="Withdrawal", Client=ClienMain))
	return render(request,"otherapps/client/allprojectsrequests.html",{'values':values});

# currently we refer both urls to a duplicate page
def activeprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Active", Client=ClienMain)
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
	return render(request,"otherapps/client/activeprojects.html", {'values':values});

def completedprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Completed", Client=ClienMain) \
				| ProjectInfo.objects.filter(ReportStatus="Withdrawal", Client=ClienMain)
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
	return render(request,"otherapps/client/completedprojects.html", {'values':values});

def reportsopen(request,projectslug):
	return render(request,"otherapps/client/reportsopen.html",{'projectslug':projectslug});
def completedprojectdetails(request,projectslug):
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	AdminFullName=Employee.objects.get(pk=values.Admin).FullName
	return render(request,"otherapps/client/completedprojectdetails.html",{'values':values, 'projectslug':projectslug, 'AdminFullName':AdminFullName});

def alldiscussions(request):
	return render(request,"otherapps/client/alldiscussions.html");
# def allsuggestions(request):
# 	return render(request,"otherapps/client/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/client/allmessages.html");


# def trial(request):
# 	return render(request,"otherapps/client/trial.html",{'values':values});





