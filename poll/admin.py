from django.contrib import admin
from models import PollStat

# Register your models here.
class PollStatAdmin(admin.ModelAdmin):
	list_display = ('name','time','count')
	search_fields=["name"]
admin.site.register(PollStat, PollStatAdmin)
