komey_cache = {}

def put_in_cache(key, val):
	global komey_cache
	komey_cache[key] = val
	#print "After putting %s, cache is %s" % (key, komey_cache)
	
def get_from_cache(key, default=None):
	return komey_cache.get(key, default)

def remove_from_cache(key):
	global komey_cache
	komey_cache.pop(key, None) #will return None if key not present
	#print "After removing %s, cache is %s" % (key, komey_cache)

def remove_terminal_from_list(nick):
	global komey_cache
	terminals = komey_cache.get('terminals', [])
	try:
		terminals.remove(nick)
		put_in_cache('terminals', terminals)
	except Exception, e:
		print str(e)	

def add_terminal_to_list(nick):
	global komey_cache
	terminals = komey_cache.get('terminals', [])	
	terminals.append(nick)
	put_in_cache('terminals', terminals)

def user_put_in_cache(action_args, user_args):
	global komey_cache
	key = user_args['key'].strip()
	val = user_args['val'].strip()
	put_in_cache(key, val)

def user_remove_from_cache(action_args, user_args):
	global komey_cache
	key = user_args['key'].strip()
	remove_from_cache(key)
	
def clear_cache(action_args=None, user_args=None):
	global komey_cache
	komey_cache = {}
	print "Cache cleared, cache is now %s" % komey_cache
