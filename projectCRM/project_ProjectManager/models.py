from django.db import models
from project_HR.models import Employee
from project_Client.models import ProjectInfo,DeveloperBox
# Create your models here.


class AllTasks(models.Model):
	ProjectID = models.IntegerField();
	ReceiverID = models.IntegerField(default=None, null=True);
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	TaskStatus = models.BooleanField(default=False);
	def __str__(self):
		project = ProjectInfo.objects.get(pk=self.ProjectID).ProjectName
		tempPM = ProjectInfo.objects.get(id=self.ProjectID).ProjectManager
		projectmanager = Employee.objects.get(pk=tempPM).FullName
		developer = Employee.objects.get(pk=self.ReceiverID).FullName
		return projectmanager+" assign task to "+developer+" ( Project:"+project+" )";




 

 