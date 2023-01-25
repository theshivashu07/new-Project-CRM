from django.db import models
# Create your models here.
# from datetime import datetime

class ClientInfo(models.Model):
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
	ProfilePick = models.ImageField(upload_to ='client/')
	def __str__(self):
		return self.FullName+" create's a new account.";



