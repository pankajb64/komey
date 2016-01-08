import re
import json
import os

def get_service_dict(slist_s, act):
	slist_str =  re.sub("\\b,?and\\b", ',', slist_s)
	service_list = [ (key.strip(), val.strip()) for key, val in (item.split('-') for item in slist_str.strip().split(',') if item.strip()) ]
	service_dict = [ dict([('scvtype', tup[0]), ('sid', tup[1]), ('act', act)]) for tup in service_list ]
	#service_list = dict(key.strip(), val.strip() for key, val in (item.split('-') for item in slist_str.strip().split(',') if not item.strip() ))
	return service_dict
