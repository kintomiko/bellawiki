from django.shortcuts import render
import models
import Loginer
import datetime, simplejson
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def get_date_json(request):
	deltah = int(request.GET.get('hour'))
	rst = {}
	if deltah == None:
		times = models.PollStat.objects.values('time').distinct().order_by('time')
	else:
    		enddate = datetime.datetime.now()
		startdate = enddate - datetime.timedelta(hours=deltah)
		times = models.PollStat.objects.values('time').distinct().filter(time__range=[startdate, enddate]).order_by('time')
	
	rst['labels']=[]
	for dt in times:	
		rst['labels'].append((dt['time']+datetime.timedelta(hours=8)).strftime('%m-%d %H:%M:%S'))
	
	rst['datasets']=[]
	names = models.PollStat.objects.values('name').distinct()
	for name in names:
		set = {}
		set['label']=name['name']
		if deltah==None:
			objs = models.PollStat.objects.filter(name=name['name']).order_by('time')
		else:
			objs = models.PollStat.objects.filter(name=name['name'], time__range=[startdate, enddate]).order_by('time')
		set['data']=[]
		for o in objs:
			set['data'].append(o.count)
		#if set['data'][-1]>15000:
		rst['datasets'].append(set)
	return HttpResponse(simplejson.dumps(rst))

def refresh(request):
	url = 'http://rs.ewang.com/fengyun/hou.php?bangid=0001&jiangid=0010&time=1426870745&userid=000023089&sig=16cc4ac58060ca1a34531d5058b4d488'
	s = Loginer.Session();
	res = s.open(url)
	data = eval(res.read())
	time = datetime.datetime.now()
	for d in data['data']:
		item = models.PollStat.objects.create(count = int(d['piao']), name=d['name'], time=time)
		item.save()
	return HttpResponse('success')

