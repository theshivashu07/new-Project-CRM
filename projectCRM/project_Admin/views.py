from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
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

def allprojectsrequests(request):
	# Below we use developer because it is the last thing wheich we insert... otherwise also use ProjectManager=None...
	# datasets=ProjectInfo.objects.filter(Developer=None, ReportStatus="Active", Admin='1')
	datasets=ProjectInfo.objects.filter(ReportStatus="Active", Admin=AdminMain)
	values=list()
	for dataset in datasets:
		newdict=dict()
		# put all original data's...
		newdict['original']=dataset;
		# get-n-put all duplicate data's...
		temp=ClientInfo.objects.get(pk=dataset.Client).FullName
		newdict['duplicate']={'ClientsFullName':temp};
		values.append(newdict)
	return render(request,"otherapps/admin/allprojectsrequests.html",{'values':values});

def projectdetailsslug(request,projectslug):
	if request.method=="POST":
		lock=ProjectInfo.objects.get(pk=request.POST["projectID"])
		if(request.POST["projectmanager"]): 
			lock.ProjectManager=request.POST["projectmanager"];
			lock.save()
		if(request.POST["developer"]):
			values=DeveloperBox()
			lock.Developer+=1
			lock.save()
			values.ProjectInfosID=lock
			values.DeveloperID=request.POST["developer"];
			values.save()
		return redirect('/projectdetails/'+projectslug)
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
	print(values)
	return render(request,"otherapps/admin/projectdetails.html", {'values':values, 'ClientFullName':ClientFullName, 'path':request.path,
		'projectmanagerslist':projectmanagerslist, 'developerslist':developerslist, 'selectedprojectmanager':selectedprojectmanager , 'selecteddeveloperslist':selecteddeveloperslist});

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
	ClientFullName=ClientInfo.objects.get(pk=values.Client).FullName
	return render(request,"otherapps/admin/projectdetails_editorassignnew.html",{'values':values, 'path':request.path,'ClientFullName':ClientFullName});





# currently we refer both urls to a duplicate page
def activeprojects(request):
	# values=ProjectInfo.objects.get(pk=AdminMain)
	values=ProjectInfo.objects.filter(ReportStatus="Active", Admin=AdminMain)
	print(values)
	for value in values:
		if(value.Client):
			value.Client=ClientInfo.objects.get(pk=value.Client).FullName
		if(value.Admin):
			value.Admin=Employee.objects.get(pk=value.Admin).FullName
		if(value.ProjectManager):
			value.ProjectManager=Employee.objects.get(pk=value.ProjectManager).FullName
		if(value.Developer):
			locks=DeveloperBox.objects.filter(ProjectInfosID=value.id)
			for lock in locks:
				temp=Employee.objects.get(pk=lock.id)
				lock.FullName=temp.FullName
				lock.ProfilePick=temp.ProfilePick
			value.Developer=locks
	return render(request,"otherapps/admin/activeprojects.html", {'values':values});
def completedprojects(request):
	return render(request,"otherapps/admin/completedprojects.html");

# new 
def recruitments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/admin/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/admin/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/admin/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/admin/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/admin/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/admin/allmessages.html");

def reportscollection(request):
	return render(request,"otherapps/admin/reportscollection.html");
def sendreports(request):
	return render(request,"otherapps/admin/sendreports.html");
def sendreportsopen(request,username):
	return render(request,"otherapps/admin/sendreportsopen.html");
def creativeteam(request):
	return render(request,"otherapps/admin/creativeteam.html");


