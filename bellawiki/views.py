from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import urllib, datetime
import models, forms, lunar
import Loginer
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import simplejson
from time import strftime
from django.db.models import Count
from django.db.models import Q

from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import BasicAuthentication
# api views

from rest_framework.authentication import SessionAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Serializers define the API representation.
class WorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Work
        fields = ('id', 'date', 'type', 'title', 'desc')

# ViewSets define the view behavior.
class WorkViewSet(viewsets.ModelViewSet):
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    tc = datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=8, weeks=0)
    queryset = models.Work.objects.filter(date__isnull=False, date__month = tc.month, date__day = tc.day).order_by('date')
#    queryset = models.Work.objects.all()
    serializer_class = WorkSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'works', WorkViewSet)





# Create your views here.

def create_or_edit_work(request):
	wtitle = request.GET.get('wtitle')
	if wtitle == None or wtitle == '':
		return HttpResponseRedirect('/bellawiki/')
	works = models.Work.objects.filter(title=wtitle)
	if len(works) == 0:
		if request.user.is_authenticated():
			work = models.Work.objects.create(title=wtitle)
		else:
			return HttpResponseRedirect('/accounts/login/?next='+'/bellawiki/work_details?wtitle='+wtitle)
	else:
		work = works[0]
	work_form = forms.WorkForm(instance=work)
	file_input_form = forms.FileForm()
	return render(request, 'work_detals.html', {'work':work, 'work_form':work_form, 'file_input_form':file_input_form})

def edit_file(request):
	# md5 = request.GET.get('md5')
	id=int(request.GET.get('id'))
	name=request.GET.get('name')
	if name!=None and id == None:
		file, created = models.File.objects.get_or_create(name=name)
	else:
		file = get_object_or_404(models.File, id=id)
	file_form = forms.FileForm(instance=file)
	return render(request, 'file_details.html', {'file':file, 'file_form':file_form})

@login_required
def save_file(request):
	# md5 = request.POST.get('md5')
	id=int(request.POST.get('id'))
	file = get_object_or_404(models.File, id=id)
	file_form = forms.FileForm(request.POST, instance=file)
	file_form.save()
	return HttpResponse('success')

@login_required
def add_file(request):
	wtitle = request.POST.get('wtitle')
	work = get_object_or_404(models.Work, title=wtitle)
	files = models.File.objects.filter(md5=request.POST.get('md5'))
	if len(files)==0:
		file_form = forms.FileForm(request.POST)
		file = file_form.save()
	else:
		file = files[0]
	work.files.add(file)
	return HttpResponse('success')

@login_required
def save_work(request):
	wtitle = request.POST.get('title')
	work = get_object_or_404(models.Work, title=wtitle)
	work_form = forms.WorkForm(request.POST, instance=work)
	work_form.save()
	return HttpResponse('success')

@login_required
def add_work_tag(request):
	wtitle = request.POST.get('wtitle')
	name = request.POST.get('name')
	work = get_object_or_404(models.Work, title=wtitle)
	tag, created = models.Tag.objects.get_or_create(name=name, type=models.Tag.WORK)
	work.tags.add(tag)
	tag.save()
	return HttpResponse('success')

@login_required
def del_work_tag(request):
	wtitle = request.POST.get('wtitle')
	name = request.POST.get('name')
	work = get_object_or_404(models.Work, title=wtitle)
	tag = get_object_or_404(models.Tag, name=name, type=models.Tag.WORK)
	work.tags.remove(tag)
	return HttpResponse('success')

@login_required
def add_file_tag(request):
	id = request.POST.get('id')
	name = request.POST.get('name')
	file = get_object_or_404(models.File, id=id)
	tag, created = models.Tag.objects.get_or_create(name=name, type=models.Tag.FILE)
	file.tags.add(tag)
	tag.save()
	return HttpResponse('success')

@login_required
def del_file_tag(request):
	id = request.POST.get('id')
	name = request.POST.get('name')
	file = get_object_or_404(models.File, id=id)
	tag = get_object_or_404(models.Tag, name=name, type=models.Tag.FILE)
	file.tags.remove(tag)
	return HttpResponse('success')

@login_required
def proxy(request):
	url = urllib.unquote(request.GET.get('url'))
	print url
	request = Loginer.HttpRequest()
	request.url=url
	request.header={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2,zh-TW;q=0.2',
		'Connection':'keep-alive',
		'Host':'pan.baidu.com',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_90_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'
	}
	s = Loginer.Session()
	res = Loginer.get(s, request)
	con = res.read()
	return HttpResponse(con)

def search_work(request):
	key = request.POST.get('search_key')
	works = models.Work.objects.filter(title__icontains=key).order_by('title')
	files = models.File.objects.filter(name__icontains=key).order_by('name')
	return render(request, 'work_list.html', {'works':works, 'key':key, 'files':files})

def index(request):
	return render(request, 'index.html')

def tag_index(request):
	tags = models.Tag.objects.annotate(num_work=Count('works'), num_file=Count('files')).filter(Q(num_work__gt=3)|Q(num_file__gt=3)).order_by('type')
	return render(request, 'tag_index.html', {'tags': tags})

@staff_member_required
def upload_list(request):
	return render(request, 'upload.html')

def get_by_display(model, field_name, value):
	choices = model._meta.get_field(field_name).choices
	for c in choices:
		if value == c[1]:
			return c[0]

def up(request):
	wtitle = request.POST.get('wtitle')
	work = get_object_or_404(models.Work, title=wtitle)
	work.up+=1
	work.save()
	return HttpResponse('success')

@staff_member_required
def upload(request):
	csv_string = urllib.unquote(request.POST.get('file')).encode('utf8')
	if csv_string:
		# print csv_string
		lines = csv_string.split('\t')
		for line in lines:
			if len(line)<1:
				continue
			row = line.split(',')
			if len(row)<8:
				continue
			if row[8]==None or row[8]=='':
				file = models.File.objects.create()
				created=True
			else:
				file, created = models.File.objects.get_or_create(md5 = row[8])
			if created:
				file.url=row[1]
				file.type=get_by_display(models.File, 'type', row[2])
				file.quality=get_by_display(models.File, 'quality', row[3])
				file.desc=row[5]
				if row[6]!='':
					file.date=row[6]
				file.name=row[7]
				file.save()
			if row[0]!=None and row[0]!='':
				work, created = models.Work.objects.get_or_create(title=row[0])
				work.files.add(file)
			tags=row[4].split(';')
			for tag_name in tags:
				if tag_name=='':
					continue
				tag, created = models.Tag.objects.get_or_create(name=tag_name, type=models.Tag.FILE)
				file.tags.add(tag)

		return HttpResponse('success')
	else:
		return HttpResponse('need csv! ')

def today(request):
	tc = datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=8, weeks=0)
	next_tc = datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=32, weeks=0)
	works = models.Work.objects.filter(date__isnull=False, date__month = tc.month, date__day = tc.day).order_by('date')
	next_works = models.Work.objects.filter(date__isnull=False, date__month = next_tc.month, date__day = next_tc.day).order_by('date')
	current = lunar.get_lunar_date(tc.year, tc.month, tc.day)
	tworks = models.Work.objects.filter(date__isnull=False).order_by('date')
	def lunare(x):
		td = lunar.get_lunar_date(x.date.year, x.date.month, x.date.day)
		if td[1] == current[1] and td[2] == current[2]:
			return True
		else:
			return False
	lworks = filter(lunare, tworks)
	return render(request, 'today.html', {'works':works,'lworks':lworks,'tworks':next_works})

def time_line(request):
	return render(request, 'timeline.html')

def file_timeline_json(request):
	year=int(request.GET.get('year'))
	if year==None or year=='':
		works = models.Work.objects.filter(date__isnull=False).order_by('date')
	else:
		if year == 1999:
			works = models.Work.objects.filter(date__isnull=False, date__lt=datetime.date(2000, 1, 1)).order_by('date')
		else:
			works = models.Work.objects.filter(date__isnull=False, date__year=year).order_by('date')
	rst = []
	for work in works:
		workj = {}
		# workj['title']=file.name
		workj['date']=work.date.strftime("%d %b %Y")
		workj['displaydate']=work.date.strftime("%d %b %Y")
		workj['up']=work.up
		# workj['caption']=file.desc
		body = work.title
		if len(work.files.all()) == 0:
			workj['innerclass']='nofile'
		else:
			workj['innerclass']='yesfile'
		workj['body']=body
		workj['readmoreurl']='/bellawiki/work_details/?wtitle='+work.title
		rst.append(workj)
	return HttpResponse(simplejson.dumps(rst))


# def get_info(request):
# 	url = request.GET.get('furl')
# 	s = Loginer.Session()
# 	res = s.open(url)
# 	con = res.read()
# 	md5 = con[con.rfind('md5')+6:con.rfind('md5')+38]
# 	return HttpResponse('md5')
