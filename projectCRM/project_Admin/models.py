from django.db import models
# Create your models here.
from project_HR.models import Employee
from project_Client.models import ClientInfo,ProjectInfo,DeveloperBox
# from project_Admin.models import ReportsOrMessages

class ReportsOrMessages(models.Model):
	ProjectID = models.IntegerField();
	WhatIsIt = models.CharField(max_length=25);		# Report or Message
	SenderID = models.IntegerField();
	SenderRole = models.CharField(max_length=25);  		# Project Manager / Developer
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	def __str__(self):
		return self.SenderRole+" sending a "+self.SenderRole+" to XYZ Project. ( ID:"+str(self.id)+', Date:'+str(self.SendingDateTime)+" )";

class AllMessages(models.Model):
	'''Well, here chats feature i'm giving to only employees, else tracking problems happens...'''
	SenderID = models.IntegerField();
	# isSenderClient = models.BooleanField(default=False);  		# Client or Else
	ReceiverID = models.IntegerField();
	# isReceiverClient = models.BooleanField(default=False);  	  # Client or Else
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	def __str__(self):
		sender = Employee.objects.get(pk=self.SenderID).FullName
		receiver = Employee.objects.get(pk=self.ReceiverID).FullName
		return sender+" sending a message to "+receiver+". ( ID:"+str(self.id)+', Date:'+str(self.SendingDateTime)+" )";

class AllSuggestions(models.Model):
	ProjectID = models.IntegerField();
	SenderID = models.IntegerField(default=None, null=True);
	SenderRole = models.CharField(max_length=25);  		# Client or Else
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	def __str__(self):
		project = ProjectInfo.objects.get(pk=self.ProjectID).ProjectName
		TheNameOfClass = locals()[  'ClientInfo' if(self.SenderRole=="Client") else 'Employee' ]
		sender = TheNameOfClass.objects.get(pk=self.SenderID).FullName
		return sender+" gives a suggestion on "+project+" project. ( ID:"+str(self.id)+', Date:'+str(self.SendingDateTime)+" )";




