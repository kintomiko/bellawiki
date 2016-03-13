from django.forms import ModelForm, Textarea, TextInput
from . import models

class WorkForm(ModelForm):
    class Meta:
        model = models.Work
        fields = ['title', 'type', 'desc', 'date']
        widgets = {
            'desc': Textarea(attrs={'cols': 100, 'rows': 20}),
            'title': TextInput(attrs={'readonly':'readonly'}),
        }

class TagForm(ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name']

class FileForm(ModelForm):
    class Meta:
        model = models.File
        fields = ['name', 'desc', 'md5', 'url', 'type','quality', 'date']
        widgets = {
            'desc': Textarea(attrs={'cols': 100, 'rows': 10}),
        }
