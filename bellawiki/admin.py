from django.contrib import admin
from models import File, Work, Tag

class WorkAdmin(admin.ModelAdmin):
    list_display = ("title", "desc")
    search_fields=["title"]

class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "desc", "md5", "url", "date")
    search_fields=["name"]

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "type")

admin.site.register(File, FileAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Tag, TagAdmin)
