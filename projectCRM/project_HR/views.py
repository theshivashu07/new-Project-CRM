from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Employee
from project_Client.models import ClientInfo,ProjectInfo
# from django.utils import timezone
from django.db.models import Q


'''
def index(request):
	return HttpResponse("This is <b>HR</b> page!!!");
'''

def index(request):
	return render(request,"otherapps/hr/index.html");

def myaccount(request):
	return render(request,"otherapps/hr/myaccount.html");
def myconnections(request):
	return render(request,"otherapps/hr/myconnections.html");
def mydeactivate(request):
	return render(request,"otherapps/hr/mydeactivate.html");
def mynotification(request):
	return render(request,"otherapps/hr/mynotification.html");


def allprojectsrequests(request):
	# values=ProjectInfo.objects.all().values('id')
	datasets=ProjectInfo.objects.filter(ReportStatus="Not Received")
	values=list()
	for dataset in datasets:
		newdict=dict()
		# put all original data's...
		newdict['original']=dataset;
		# get-n-put all duplicate data's...
		temp=ClientInfo.objects.get(pk=dataset.Client).FullName
		newdict['duplicate']={'ClientsFullName':temp};
		values.append(newdict)
	return render(request,"otherapps/hr/allprojectsrequests.html",{'values':values});

# currently we refer both urls to a duplicate page
def activeprojects(request):
	return render(request,"otherapps/hr/activeprojects.html");
def reportsopen(request,username):
	return render(request,"otherapps/hr/reportsopen.html");
def completedprojects(request,username=None):
	if(username!=None):
		# default assignment 
		values=ProjectInfo.objects.get(pk=5)
		return render(request,"otherapps/hr/projectdetails_withteam.html",{'values':values});
	return render(request,"otherapps/hr/completedprojects.html");


def projectdetails(request):
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
		# return redirect('request,"otherapps/hr/projectdetails.html"');
		return render(request,"otherapps/hr/projectdetails_editorassignnew.html");
	clientID=1
	return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'clientID':clientID});
	# return render(request,"otherapps/hr/projectdetails_foractive.html");

def projectdetailsslug(request,projectslug):
	AdminsFullName=None
	if request.method=="POST":
		AdminsFullName=request.POST["admin"];
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	ClientFullName=ClientInfo.objects.get(pk=values.Client).FullName
	return render(request,"otherapps/hr/projectdetails_proceed.html",{'values':values, 'ClientFullName':ClientFullName, 'AdminsFullName':AdminsFullName});

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
		return redirect('/'+prevPATH)
		# return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'values':lock});
	# get key from url's slug ---> 'shivam-shukla-77' to '77'...
	key=int(projectslug.split('-')[-1])
	values=ProjectInfo.objects.get(pk=key)
	# --------------------------------------------------------------
	# NOTE : below we are getting our previous url...
	# print(request.META.get('HTTP_REFERER'))
	overallURL=request.META['HTTP_REFERER']
	orignalURL=overallURL[22:]  #''.join(overallURL.split('/')[3:])
	return render(request,"otherapps/hr/projectdetails_editorassignnew.html",{'values':values, 'prevPATH':orignalURL});




# new 
def recruitments(request):
	if request.method=="POST":
		values=Employee(
			Username = request.POST["username"],
			Password = request.POST["password"],
			FirstName = request.POST["firstname"],
			LastName = request.POST["lastname"],
			FullName = request.POST["firstname"]+' '+request.POST["lastname"],
			EmailId = request.POST["emailid"],
			MobileNo = request.POST["mobileno"],  # str(int(request.POST["mobileno"])+1),
			Language = 'Hindi',
			Address = request.POST["address"],
			ZipCode = 489827,
			State = request.POST["state"],
			Country = request.POST["country"],
			Company = request.POST["company"],
			EmploymentID = request.POST["employmentid"],
			As = request.POST["as"],
			Role =request.POST["role"],
			Level = request.POST["level"],
			OfficeLocation = request.POST["officelocation"],
			SittingArea = request.POST["sittingarea"],
			JoiningBeginningDate = request.POST["joiningbeginningdate"],
			JoiningEndingDate = request.POST["joiningendingdate"],
			Salary = request.POST["salary"],
			Contract = request.POST["contract"],
			CTC = request.POST["ctc"], );
		values.save()
		# return redirect('/trialcenter/'+str(values.id))
		# values=Employee.objects.get(pk=values.id)
		return render(request,"otherapps/hr/recruitments.html",{'values':values});
	return render(request,"otherapps/hr/recruitments.html");
def promotions(request):
	dataset=["Project Manager","Developer"]
	return render(request,"otherapps/hr/promotions.html");
def increments(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/hr/increments.html");
def decrements(request):
	dataset=["Admin","Project Manager","Developer"]
	return render(request,"otherapps/hr/decrements.html");
def pick(request,target):
	print(request.path,target)
	dataset=["Admin","Project Manager","Developer"]
	pickfromtarget={'promotions':'Pramote','increments':'Increment','decrements':'Decrement'}
	return render(request,"otherapps/hr/searching4pid.html",{"targetedpath":target,"targetedfrom":pickfromtarget[target]});

def alldiscussions(request):
	return render(request,"otherapps/hr/alldiscussions.html");
def allsuggestions(request):
	return render(request,"otherapps/hr/allsuggestions.html");
def allmessages(request):
	return render(request,"otherapps/hr/allmessages.html");



def trialcenter(request,key):
	print(key)
	values=Employee.objects.get(pk=int(key))
	# return render(request,"otherapps/hr/recruitments.html",{'values':values});
	return render(request,"otherapps/hr/trialcenter.html",{'values':values});




