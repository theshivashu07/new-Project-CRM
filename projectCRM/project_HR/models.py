from django.db import models
# Create your models here.
from autoslug import AutoSlugField


class Employee(models.Model):
	Username = models.CharField(max_length=25);
	Password = models.CharField(max_length=25);
	FirstName = models.CharField(max_length=25);
	LastName = models.CharField(max_length=25);
	FullName = models.CharField(max_length=50);
	EmailId = models.CharField(max_length=30);
	MobileNo = models.IntegerField()
	Language = models.CharField(max_length=30, default=None, null=True);
	Address = models.CharField(max_length=50);
	ZipCode = models.IntegerField(default=None, null=True)
	State = models.CharField(max_length=25);
	Country = models.CharField(max_length=25);
	ProfilePick = models.ImageField(upload_to ='client/',max_length=75,default=None)

	Company = models.CharField(max_length=100)
	EmploymentID = models.CharField(max_length=100)
	As = models.CharField(max_length=50)
	Role = models.CharField(max_length=100)
	Level = models.IntegerField()
	OfficeLocation = models.CharField(max_length=100)
	SittingArea = models.CharField(max_length=100)
	# JoiningDate, LeavingDate
	JoiningBeginningDate = models.DateField(default=None, null=True);
	JoiningEndingDate = models.DateField(default=None, null=True);
	Salary = models.IntegerField();
	Contract = models.CharField(max_length=20);  # in years
	CTC = models.CharField(max_length=250);

	JoiningDate = models.DateTimeField(auto_now_add=True);
	UpdationDate = models.DateTimeField(auto_now=True);
	def __str__(self):
		return self.FullName+" ("+self.Role+") join us, as "+self.As+".";

















