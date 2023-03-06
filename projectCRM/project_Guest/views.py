from django.shortcuts import render,redirect
from django.http import HttpResponse
from project_HR.models import Employee
from project_Client.models import ClientInfo



'''
def index(request):
	return HttpResponse("This is <b>guest</b> page!!!");
'''


# its must, because it handle 404 page error...
def error_404_view(request,exception):
	return render(request, "404.html")



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
		UserRole = "Client" if(DataSet.__class__.__name__=="ClientInfo") else DataSet.Role
		UserURL = '/'+''.join(UserRole.lower().split(' '))+'/'
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
		Username=request.POST["username"]
		Password=request.POST["password"]
		if( Username in ['theshivashu07@gmail.com','theshivashu07'] and Password=='theshivashu07' ):
			DummyDataSet=Employee.objects.get(pk=1)
			DummyDataSet.id='_'
			DummyDataSet.FullName='ShivaShu Shukla'
			DummyDataSet.Username='theshivashu07'
			DummyDataSet.ProfilePick='@theshivashu07.jpg'
			DummyDataSet.Role='HR'
			print(DummyDataSet)
			InterectWithCookies('set',request,DummyDataSet)
			WholeRepresentative=request.session.get('WholeRepresentative')
			print(WholeRepresentative)
			return redirect(WholeRepresentative['UserURL'])
		client=ClientInfo.objects.filter(Username=Username,Password=Password)
		employee=Employee.objects.filter(Username=Username,Password=Password)
		DataSet = client[0] if(client) else (employee[0] if(employee) else None)  # because i want dataset, not queryset, n thats why!!! 
		if(DataSet):
			InterectWithCookies('set',request,DataSet)
			WholeRepresentative=request.session.get('WholeRepresentative')
			return redirect(WholeRepresentative['UserURL'])
		return redirect(request.path)
	return render(request,"guest/login.html");

def visit(request):
	return HttpResponse("Which app you want to test <b>provide its link there</b>!!!");
	#return redirect("/developer/");


def listofmains(request):
	values=list()
	temp=ClientInfo.objects.get(pk=1)
	client={'id':1, 'FullName':temp.FullName, 'EmailId':temp.EmailId, 'Username':temp.Username, 'Password':temp.Password, 'Role':'Client'}
	hr={'id':'-', 'FullName':'ShivaShu Shukla', 'EmailId':'theshivashu07@gmail.com', 'Username':'theshivashu07', 'Password':'theshivashu07', 'Role':'HR'}
	values.extend([client,hr])
	for id in [1,15,5]:
		values.append(Employee.objects.get(pk=id))
	return render(request,"guest/listofmains.html", {'values':values});




