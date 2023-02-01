from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ClientInfo,ProjectInfo
from project_HR.models import Employee
# from django.utils import timezone
from django.db.models import Q




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
def clientdetails(request):
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
	return render(request,"otherapps/client/clientdetails.html");

def projectdetails(request,projectslug=None):
	print("Radhy-Radhy...")
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
		# return redirect('request,"otherapps/client/projectdetails.html"');
		return render(request,"otherapps/client/projectdetails.html");
	clientID=1
	return render(request,"otherapps/client/projectdetails.html",{'clientID':clientID});
def clientconnections(request):
	return render(request,"otherapps/client/clientconnections.html");
def clientdeactivate(request):
	return render(request,"otherapps/client/clientdeactivate.html");
def clientnotification(request):
	return render(request,"otherapps/client/clientnotification.html");
def allprojectsrequests(request):
	# values=ProjectInfo.objects.all().values('id')
	values=reversed(ProjectInfo.objects.filter(~Q(ReportStatus="Completed")))
	return render(request,"otherapps/client/allprojectsrequests.html",{'values':values});

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/client/activeprojects.html");
def reportsopen(request,username):
	return render(request,"otherapps/client/reportsopen.html");
def completedprojects(request):
	return render(request,"otherapps/client/completedprojects.html");
def projectdetailsopen(request,username):
	return render(request,"otherapps/client/projectdetails.html");


# def trial(request):
# 	print("Radhy-Radhy...")
# 	if request.method=="POST":
# 		values=ProjectInfo.objects.get(pk=3);
# 		values.Client=request.POST["clientID"];
# 		values.ProjectName=request.POST["projectname"];
# 		values.ProgrammingLanguage=request.POST["programminglanguage"];
# 		values.FrontEnd=request.POST["frontend"];
# 		values.BackEnd=request.POST["backend"];
# 		values.DataBase=request.POST["database"];
# 		values.BeginningDate=request.POST["beginningdate"];
# 		values.EndingDate=request.POST["endingdate"];
# 		values.StartingAmount=request.POST["startingamount"];
# 		values.EndingAmount=request.POST["endingamount"];
# 		values.SoftDiscription=request.POST["softdiscription"];
# 		values.save()
# 		return render(request,"otherapps/client/trial.html");
# 	values=ProjectInfo.objects.get(pk=3) 
# 	return render(request,"otherapps/client/trial.html",{'values':values});





