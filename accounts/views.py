#Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from manager import cache_manager, proxy_manager
import simplejson
import random
from models import Proxy

class RET_CODE:
	STARTED='100'
	SUCCESS='200'
	IN_PROGRESS='201'
	STOP='300'
	PAUSE='301'
	ERROR='500'
	NOT_SUPPORT='501'

DZMF_DOMAIN='dzwm'

def genPost():
	netease={}
	ip_str = ''
	for i in range(4):
		ip_str+=str(int(random.random()*255))+'.'

	ip_str = ip_str[:-1]
	netease['post'] = 'voterId='+ip_str+'&votedId=153&ip='+ip_str
	netease['url']='http://dzmf.wenming.cn/point.do'

	netease['header']={
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2,zh-TW;q=0.2',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Host':'dzmf.wenming.cn',
	'Origin':'http://dzmf.wenming.cn',
	'Referer':'http://dzmf.wenming.cn',
	'User-Agent':'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_0likeMacOSX;en-us)AppleWebKit/532.9(KHTML,likeGecko)Version/4.0.5Mobile/8A293Safari/6531.22.7',
	'X-Requested-With':'XMLHttpRequest'
	}
	return netease

def root(request):
	return render(request, 'root.html')

def verify_dzwm(request):
	id = request.GET.get('id')
	rst = cache_manager.get(DZMF_DOMAIN, id)
	try:
		if rst is None:
			cache_manager.set(DZMF_DOMAIN, id, RET_CODE.STARTED);
			return HttpResponse(RET_CODE.STARTED)
		elif str(rst)==RET_CODE.PAUSE:
			return HttpResponse(RET_CODE.PAUSE)
		elif str(rst)==RET_CODE.STOP:
			return HttpResponse(RET_CODE.STOP)
		else:
			return HttpResponse(RET_CODE.IN_PROGRESS)
	except Exception as e:
		print str(e.message)
		return HttpResponse(RET_CODE.ERROR)

def view_create_cache(request, domain):
	if request.method == 'GET':
		rst = cache_manager.all(domain)
		return HttpResponse(simplejson.dumps(rst))
	elif request.method == 'PUT':
		cache_manager.create(domain)
		return HttpResponse(RET_CODE.SUCCESS)
	return HttpResponse(RET_CODE.NOT_SUPPORT)

def set_cache(request, domain, machine_id):
	if request.method == 'POST':
		request_dict = eval(request.body)
		cache_manager.set(domain, machine_id, request_dict);
	return HttpResponse(RET_CODE.NOT_SUPPORT)

def get_dzwm(request):
	return HttpResponse(simplejson.dumps(genPost()))

def del_proxy(request):
	url = request.GET.get('url')
	if url is None or url=='':
		return HttpResponseNotFound('failed')
	proxy = Proxy.objects.get(url=url)
	proxy.delete()
	return HttpResponse('success')

def get_proxy(request):
	num = request.GET.get('num')
	if num>0:
		proxies = Proxy.objects.all().order_by('?')[0:num]
		return HttpResponse(reduce(lambda x,y:x+'\r\n'+y,[p.url for p in proxies]))
	return HttpResponseNotFound('failed')

def add_proxy(request):
	urls = request.body
	print urls
	urlList = urls.split(',')
	rst=[]
	for url in urlList:
		try:
			p = Proxy(url = url, rate=0)
			p.save()
		except Exception as e:
			print rst.append(e.message)
			continue
	return HttpResponse(reduce(lambda x,y:x+','+y, rst))

def set_all_dzwm(request):
	status = request.GET.get('status')
	dzwm = cache_manager.all(DZMF_DOMAIN)
	if dzwm is not None:
		for k in dzwm.keys():
			dzwm[k]=status
		cache_manager.set_all(DZMF_DOMAIN, dzwm)
	return HttpResponse('success')
