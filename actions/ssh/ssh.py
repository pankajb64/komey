import json
import pxssh
from actions.komey_util.komey_cache import get_from_cache, put_in_cache, remove_from_cache, add_terminal_to_list, remove_terminal_from_list
import os
from bcolors import bcolors

def ssh_login(action_args, user_args):
	credentials_file = os.getcwd() + '/data/credentials/' + user_args['credentials'].strip()
	#print credentials_file
	host = user_args['host'].strip()
	nick = user_args.get('nick', '')
	nick = nick.strip() if nick is not None else 'unk'
	credentials = {}
	with open(credentials_file, 'rb') as f:
		credentials = json.load(f)
	#print credentials
	ssh = pxssh.pxssh(timeout=120)
	ssh.login(host, credentials['username'], credentials['password'])
	#ssh.prompt()
	print "logged in successfully"
	put_in_cache(nick, ssh)
	put_in_cache(nick+"_sudo_password", credentials['password'])
	add_terminal_to_list(nick)
	put_in_cache('terminal', nick) #make this the active terminal


def ssh_logout(action_args, user_args):
	nick = user_args.get('nick')
	#print "Got Nick %s" %nick
	if nick is None:
		nick = get_from_cache('terminal')
	terminal = get_from_cache(nick.strip())
	if terminal is not None:
		#from komey.util.bcolors import bcolors
		#print "Logging out from %s" % nick
		terminal.logout()
		put_in_cache('terminal', None)
	else:
		#from komey.util.bcolors import bcolors
		print "%sWARNING - No such terminal %s%s" %(bcolors.WARNING, nick, bcolors.ENDC)	
	if nick is not None:
		remove_terminal_from_list(nick)
		remove_from_cache(nick)
	#print "Completed"	
	
def ssh_logout_all(action_args, user_args):
	terminals = get_from_cache('terminals', [])
	print "Closing these terminals %s" % terminals
	for my_nick in list(terminals):
		#print "Closing %s" %my_nick
		new_dict =  { 'nick' : my_nick }
		ssh_logout(action_args, new_dict)
		#print get_from_cache('terminals')		
