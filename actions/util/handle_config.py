from actions.komey_util.komey_cache import komey_cache
config_file = ""
config_dict = {}

def write_config(action_args, user_args):
	with open(config_file, 'wb') as f:
		json.dump(config_dict, f)

def load_config(config_file):
	print "File is %s" % config_file
	with open(config_file, 'rb') as f:
		config_dict = json.load(f)

def set_config(action_args, user_args):
	global config_dict
	config_dict[user_args['key'].strip()] = user_args['val'].strip()
	
def get_config(action_args, user_args):
	val = config_dict[user_args['key'].strip()]
	print val
	return val

def use_setup(action_args, user_args):
	setup = user_args['setup'].strip()
	print "Setup is %s" % setup
	global config_file
	config_file = os.getcwd() + '/data/config/' + setup + '.json'
	load_config()
	load_config_into_cache()

def load_config_into_cache(action_args=None, user_args=None):
	komey_cache.update(config_dict)
	print "Cache updated with config"
