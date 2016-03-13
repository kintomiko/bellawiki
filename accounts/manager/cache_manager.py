from django.core.cache import cache

def get(domain, key):
	domain_map = cache.get(domain)
	if domain_map is None:
		domain_map = {}
		cache.set(domain, domain_map)
	return domain_map.get(key)

def set(domain, key, value):
	domain_map = cache.get(domain)
	if domain_map is None:
		raise Exception('domain not exists')
	domain_map[key]=value
	cache.set(domain, domain_map)

def all(domain):
	domain_map = cache.get(domain)
	if domain_map is None:
		raise Exception('domain not exists')
	return domain_map

def create(domain):
	domain_map = cache.get(domain)
	if domain_map is not None:
		raise Exception('domain exists')
	domain_map = {}
	cache.set(domain, domain_map)

def set_all(domain, map):
	cache.set(domain, map)
