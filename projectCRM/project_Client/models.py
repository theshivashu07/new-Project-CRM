from django.db import models
# Create your models here.
from autoslug import AutoSlugField
from project_HR.models import Employee

class ClientInfo(models.Model):
	Username = models.CharField(max_length=25);
	Password = models.CharField(max_length=25);
	FirstName = models.CharField(max_length=25);
	LastName = models.CharField(max_length=25);
	FullName = models.CharField(max_length=50);
	EmailId = models.CharField(max_length=30);
	MobileNo = models.IntegerField()
	Organization = models.CharField(max_length=30);
	Language = models.CharField(max_length=30);
	Address = models.CharField(max_length=50);
	ZipCode = models.IntegerField()
	State = models.CharField(max_length=25);
	Country = models.CharField(max_length=25);
	# JoiningDate = models.DateTimeField(auto_now_add=True, default=timezone.now())
	JoiningDate = models.DateTimeField(auto_now_add=True)
	ProfilePick = models.ImageField(upload_to ='client/',max_length=75,default=None, null=True)
	def __str__(self):
		return self.FullName+" create's a new account, as @"+self.Username+".";


class ProjectInfo(models.Model):
	Client = models.IntegerField();
	HR = models.IntegerField(default=None, null=True);
	Admin = models.IntegerField(default=None, null=True);
	ProjectManager = models.IntegerField(default=None, null=True);
	Developer = models.IntegerField(default=None, null=True);  # developers count 
	ProjectName = models.CharField(max_length=50);
	ProjectSlug = AutoSlugField(populate_from='ProjectName', null=True);
	ProgrammingLanguage = models.CharField(max_length=50);
	FrontEnd = models.CharField(max_length=50);
	BackEnd = models.CharField(max_length=50);
	DataBase = models.CharField(max_length=50);
	BeginningDate = models.DateTimeField(default=None, null=True);
	EndingDate = models.DateTimeField(default=None, null=True);
	StartingAmount = models.CharField(max_length=10, default=None);
	EndingAmount = models.CharField(max_length=10, default=None);
	SoftDiscription = models.CharField(max_length=350);
	HardDiscription = models.CharField(max_length=500, default=None, null=True);
	JoiningDate = models.DateTimeField(auto_now_add=True);
	UpdationDate = models.DateTimeField(auto_now=True);
	ReportStatus = models.CharField(max_length=50, default=None, null=True);
	def __str__(self):
		# target = ClientInfo.objects.get(pk=self.Client)
		# target = ClientInfo.objects.get(1)
		return "Added a new project "+self.ProjectName+"("+str(self.id)+").";
		# return target.FullName+" added a new project "+self.ProjectName+".";


class DeveloperBox(models.Model):
	ProjectInfosID = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
	DeveloperID = models.IntegerField(default=None, null=True);
	def __str__(self):
		return "Developer Added. ("+str(self.id)+")."
		# tempadmin=Employee.objects.get(pk=self.ProjectInfosID.Admin).FullName
		# tempprojectmanager=Employee.objects.get(pk=self.ProjectInfosID.ProjectManager).FullName
		# tempdeveloper=Employee.objects.get(pk=self.DeveloperID).FullName
		# tempprojectname=ProjectInfo.objects.get(pk=self.ProjectInfosID).ProjectName
		# return tempadmin+" added "+tempdeveloper+" as developer for "+tempprojectname+" project, well "+tempprojectname+" is a project manager.";



