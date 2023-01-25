from django import forms
from .models import ClientInfo

class ClientImageInfo(forms.ModelForm):
	class Meta:
		model = ClientInfo
		fields = ('ProfilePick',)
		labels = {'ProfilePick':''}

