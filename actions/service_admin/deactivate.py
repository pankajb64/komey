import requests
import re
from service_util import get_service_dict

def deactivate(action_args, user_args):
	try:
		slist_s = user_args['slist']
		host = user_args['host'].strip()
		service_dict = get_service_dict(slist_s, 'd')
		print service_dict
		for service in service_dict:
			r = requests.get('http://'+host+'/serviceadmin/svcaction.jsp', params=service)
			print r.text
	except Exception, e:
		print "Exception %s" % str(e)	
	
def deactivate_multiple(action_args, user_args):
	print "Deactivating multiple %s %s" % (action_args, user_args)
