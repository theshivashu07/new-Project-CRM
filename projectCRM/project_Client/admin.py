from django.contrib import admin
# Register your models here.

from .models import ClientInfo
admin.site.register(ClientInfo)
# @admin.site.register(ClientInfo)
# class ImageAdmin(admin.ModelAdmin):
# 	"""docstring for ClassName"""
# 	listdisplay=['ProfilePick']
		

