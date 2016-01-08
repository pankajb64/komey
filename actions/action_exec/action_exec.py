from actions.komey_util.komey_util import exec_command as base_exec
import os
from actions.komey_util.komey_cache import put_in_cache, get_from_cache
import json

def exec_command(action_args, user_args):
	print "executing %s with args %s" % (user_args['command_file'] , user_args.get('command_args'))
	file_name = os.getcwd() + '/commands/' + user_args['command_file'].strip()
	command_args = user_args.get('command_args', "{}")
	command_dict = json.loads(command_args)
	for key, val in command_dict.iteritems():
		put_in_cache("arg_"+key, val)
	base_exec(file_name)
	
	
def set_exit_command(action_args, user_args):
	files = get_from_cache('files', [])
	input_file = files[-1]
	put_in_cache(input_file+'_exit_command', os.getcwd() + '/commands/' + user_args['exit_command'].strip())
