import requests

def activate(action_args, user_args):
	try:
		slist_s = user_args['slist']
		service_dict = get_service_dict(slist_s, 'a')
		print service_dict
		for service in service_dict:
			r = requests.get('http://10.14.21.14:8080/serviceadmin/svcaction.jsp', params=service)
			print r.text
	except Exception, e:
		print "Exception %s" % str(e)	
	
