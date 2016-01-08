from actions.action_exec.action_exec import exec_command
from actions.komey_util.komey_cache import get_from_cache, put_in_cache
import json
'''
def monitor_log(action_args, user_args):
	file_path = user_args['file_path'].strip()
	command_args = { 'file_path' : file_path }
	user_args['command_args'] = json.dumps(command_args)
	user_args['command_file'] = "base/tail_f"
	exec_command(action_args, user_args)
'''
