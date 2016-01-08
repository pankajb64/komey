from actions.action_exec.action_exec import exec_command
import json
import os

def scp(action_args, user_args):
	hosts = user_args['hosts'].strip().split(",")
	files = user_args['files'].strip()
	dest = user_args['dest_dir'].strip()
	credentials_file = user_args['credentials'].strip()
	credentials_file = os.getcwd() + '/data/credentials/' + credentials_file
	credentials = {}
	with open(credentials_file, 'rb') as f:
		credentials = json.load(f)
	for host in hosts:
		arg_dest = credentials['username'].strip()+'@'+host.strip()+':'+dest
		command_args = { 'scp_password' : credentials['password'].strip(), 'scp_files_cmd' : files, 'scp_dest' : arg_dest }
		user_args['command_args'] = json.dumps(command_args)
		user_args['command_file'] = "base/scp"
		exec_command(action_args, user_args)
