from actions.shell_exec.shell_exec import shell_exec, shell_exec_expect
from actions.komey_util.komey_cache import get_from_cache
'''def change_user(action_args, user_args):
	user = user_args['user'].strip()
	command = "sudo su " + user
	expect_list = ["assword:", "#"]
	response_list = [
'''

def send_command(action_args, user_args):
	command = user_args['command']
	print "got cmd %s" %command
	count = int(user_args.get('count', 1))
	expect_str = user_args.get('expect_list')
	response_str = user_args.get('response_list')
	interact = user_args.get('interact', '')
	interact = '' if interact is None else interact.strip().lower()
	interact = True if interact == 'interact' else False
	print "interact is %s" %interact
	if expect_str is None:
		shell_exec(command, interact)
	else:
		expect_list = expect_str.strip().split(",")
		response_list = response_str.strip().split(",")
		expect_dict = { 'count' : count, 'expect_list' : expect_list, 'response_list' : response_list }
		shell_exec_expect(command, expect_dict, interact)	

'''def restart_tomcat(action_args, user_args):
	command = "/etc/init.d/tomcat restart"
'''
