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


def projectdetails(request):
	print("We are here to RUN!!!")
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
	return render(request,"otherapps/client/projectdetails.html", {'value':values, 'clientID':ClienMain});


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
		lock.HardDiscription=request.POST["harddiscription"]
		lock.save()
		return redirect('/'+prevPATH)
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	values.Admin=Employee.objects.get(pk=values.Admin).FullName
	return render(request,"otherapps/client/projectdetails_editorassignnew.html",{'values':values, 'projectslug':projectslug, 'path':request.path});


def allprojectsrequests(request):
	# values=ProjectInfo.objects.all().values('id')
	values=reversed(ProjectInfo.objects.filter(ReportStatus="Not Received", Client=ClienMain))
	# values=reversed(ProjectInfo.objects.filter(ReportStatus="Not Received", Client=ClienMain)\
					# | ProjectInfo.objects.filter(ReportStatus="Withdrawal", Client=ClienMain))
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
				temp=Employee.objects.get(pk=lock.DeveloperID)
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
				temp=Employee.objects.get(pk=lock.DeveloperID)
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
# def allsuggestions(request):
# 	return render(request,"otherapps/client/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/client/allmessages.html");


# def trial(request):
# 	return render(request,"otherapps/client/trial.html",{'values':values});





