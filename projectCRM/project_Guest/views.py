from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo



'''
def index(request):
	return HttpResponse("This is <b>guest</b> page!!!");
'''
def index(request):
	return render(request,"guest/index.html");

def workprocess(request):
	return render(request,"guest/workprocess.html");

def aboutus(request):
	return render(request,"guest/aboutus.html");

def contactus(request):
	return render(request,"guest/contactus.html");

def InterectWithCookies(passing_from,request,DataSet):
	# set - get - del
	if(passing_from=="set"):
		UserRole = "Client" if(DataSet.__class__.__name__=="Client") else DataSet.Role
		UserURL = '/'+''.join(UserRole.lower().split(' '))+'/'
		print(DataSet)
		print(DataSet.ProfilePick)
		print(str(DataSet.ProfilePick))
		WholeRepresentative={'UserRole' : UserRole,'UserURL' : UserURL,'UserID' : DataSet.id, 
			'UserUsername':DataSet.Username, 'UserFullName':DataSet.FullName, 'UserProfilePick':str(DataSet.ProfilePick)}   # MUST to put "ProfilePick's" string version
		request.session['WholeRepresentative']=WholeRepresentative
	elif(passing_from=="get"):
		pass
	elif(passing_from=="del"):
		pass
	return None

def loginMethod(request):
	if request.method=="POST":
		client=ClientInfo.objects.filter(Username=request.POST["username"],Password=request.POST["password"])
		employee=Employee.objects.filter(Username=request.POST["username"],Password=request.POST["password"])
		# DataSet = client.id if(client) else (employee.id if(employee) else None)
		DataSet = client[0] if(client) else (employee[0] if(employee) else None)
		if(DataSet):
			# print(DataSet.__class__.__name__)
			InterectWithCookies('set',request,DataSet)
			WholeRepresentative=request.session.get('WholeRepresentative')
			return redirect(WholeRepresentative['UserURL'])
		else:
			# print("Sorry... you're logged OUT.")
			pass
	return render(request,"guest/login.html");

def visit(request):
	return HttpResponse("Which app you want to test <b>provide its link there</b>!!!");
	#return redirect("/developer/");




