from django.contrib import admin
# Register your models here.
from .models import ReportsOrMessages,AllMessages,AllSuggestions
admin.site.register(ReportsOrMessages)
admin.site.register(AllMessages)
admin.site.register(AllSuggestions)



