from django.db import models
from project_HR.models import Employee
from project_Client.models import ProjectInfo,DeveloperBox
# Create your models here.


class AllTasks(models.Model):
	ProjectID = models.IntegerField();
	ReceiverID = models.IntegerField(default=None, null=True);
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	TaskStatus = models.BooleanField(default=False);  # means who having now... if developer not put : False, otherwise : True.
	IsTaskFinished = models.BooleanField(default=False);    # means overall this task finished... if this task is not finished : False, otherwise : True.
	OptionalMSG = models.CharField(max_length=250, default=None, null=True);  # optional - no use now, but in future...
	GitHubLink = models.CharField(max_length=75, default=None, null=True);
	def __str__(self):
		project = ProjectInfo.objects.get(pk=self.ProjectID).ProjectName
		tempPM = ProjectInfo.objects.get(id=self.ProjectID).ProjectManager
		projectmanager = Employee.objects.get(pk=tempPM).FullName
		developer = Employee.objects.get(pk=self.ReceiverID).FullName
		return projectmanager+" assign task to "+developer+" ( Project:"+project+" )";


 

 