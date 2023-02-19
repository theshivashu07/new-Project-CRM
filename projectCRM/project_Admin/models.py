from django.db import models
# Create your models here.

class ReportsOrMessages(models.Model):
	ProjectID = models.IntegerField();
	WhatIsIt = models.CharField(max_length=25);		# Report or Message
	SenderID = models.IntegerField();
	SenderRole = models.CharField(max_length=25);  		# Project Manager / Developer
	ContentData = models.CharField(max_length=750);
	SendingDateTime = models.DateTimeField(auto_now_add=True);
	def __str__(self):
		return self.SenderRole+" sending a "+self.SenderRole+" to XYZ Project. (ID:"+str(self.id)+' Date:'+str(self.SendingDateTime)+")";


