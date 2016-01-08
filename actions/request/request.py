import requests

def get_request(action_args, user_args):
	params_str = user_args['params'].strip()
	params = dict([ (key, val)for key, val in ( item.split("=") for item in params_str.split(","))])
	host = user_args['host'].strip()
	r = requests.get(host, params=params)
	print r.text
