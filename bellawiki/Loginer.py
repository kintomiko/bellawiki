import urllib, urllib2, cookielib, json

def removeHeaderItem(opener, name):
	opener.addheaders = [x for x in opener.addheaders if x[0] != name]

def resetHeaderItem(opener, name, value):
	removeHeaderItem(opener, name)
	opener.addheaders.append((name, value))

def post(session, request):
	for k,v in request.header.items():
		resetHeaderItem(session.opener, k, v)
	res = session.open(request.url, request.post, time_out=15)
	return res

def get(session, request):
	for k,v in request.header.items():
		resetHeaderItem(session.opener, k, v)
	res = session.open(request.url)
	return res

class HttpRequest(object):
	def __init__(self):
		self.header={}
		self.url=''
		self.post={}


class Session(object):

	def __init__(self, proxy=None, debugLevel=0):
		self.cj = cookielib.CookieJar()
		cookies = urllib2.HTTPCookieProcessor(self.cj)
		httpHandler = urllib2.HTTPHandler(debuglevel=debugLevel)
		if proxy!=None:
			proxyHandler = urllib2.ProxyHandler({'http': 'http://%s/' % proxy})
			self.opener = urllib2.build_opener(cookies, httpHandler, proxyHandler)
		else:
			self.opener = urllib2.build_opener(cookies, httpHandler)
		urllib2.install_opener(self.opener)
		del self.opener.addheaders[0]
		self.opener.addheaders.append(('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2,zh-TW;q=0.2'))
		self.opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'))
		self.opener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'))
		self.opener.addheaders.append(('Connection', 'Keep-Alive'))

	def open(self, url, data=None, time_out=20):
		if data == None:
			return self.opener.open(url, timeout=time_out)
		return self.opener.open(url, data, timeout=time_out)

	def cookie(self):
		rst=''
		for k,v in {i.name: i.value for i in self.cj}.items():
			rst += k+'='+v+';'
		if len(rst)>0:
			rst = rst[0:len(rst)-1]
		return rst

class Loginer(Session):
	def __init__(self, loginUrl, userId, pwd, chkImgUrl):
		super(Loginer, self).__init__()
		self.userId = userId 
		self.password = pwd
		self.chkImgUrl = chkImgUrl
		self.chkCode=''
		self.loginUrl=loginUrl
		self.opener.addheaders.append(('Referer', self.loginUrl))
		self.csrf='' 
		self.opener.addheaders.append(('Host', loginUrl[7:loginUrl.find('/',7)]))

	def start(self):
		return self.open(self.loginUrl)

	def getCode(self):
		return self.open(self.chkImgUrl)

	def login(self):
		self.login_data = urllib.urlencode({'userId' : self.userId, 'userPwd' : self.password, 'checkImageCode': self.chkCode, 'CSRFToken': self.csrf})
		self.opener.open(self.loginUrl, self.login_data) 


if __name__ == '__main__':
	Loginer.run()
