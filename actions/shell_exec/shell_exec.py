from actions.ssh.ssh_exec import ssh_exec, ssh_exec_expect
from actions.komey_util.komey_cache import get_from_cache, put_in_cache
import shlex, subprocess
import pexpect
from bcolors import bcolors

def run_shell_exec(action_args, user_args):
	command = user_args['command']
	shell_exec(command)
	
def shell_exec(command, interact):
	terminal = get_from_cache(get_from_cache('terminal'))
	#print "%s %s" %(command, terminal)
	if terminal is None: #execute locally
		local_exec(command, interact)
	else: #execute over ssh
		ssh_exec(command, terminal, interact)

def local_exec(command, interact):
	print "Executing locally"
	args = shlex.split(command.strip())
	print args
	try:
		output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=False)
		print "Result of executing \"%s\" is %s" % (command, output)
	except subprocess.CalledProcessError, e:
		print "%sExecution Failed for command \"%s\". Error Code is %s. Result is \n%s%s" %(bcolors.FAIL, command, e.returncode, e.output, bcolors.ENDC)	
		raise

def switch_shell(action_args, user_args):
	nick = user_args['nick']
	print "Switching to %s" % nick
	if nick.lower() == 'local':
		nick = None
	put_in_cache('terminal', nick)

def shell_exec_expect(command, expect, interact):
	terminal = get_from_cache(get_from_cache('terminal'))
	if terminal is None: #execute locally
		local_exec_expect(command, expect, interact)
	else: #execute over ssh
		ssh_exec_expect(command, expect, terminal, interact)
		
def local_exec_expect(command, expect, interact):
	print command
	process = pexpect.spawn(command.strip())
	count = expect['count']
	try:
		for i in xrange(count):
			index = process.expect(expect['expect_list'])
			print "index is is %s expect is %s before is \n%s" %(index, expect['expect_list'][index], process.before)
			process.sendline(expect['response_list'][index])
		if interact == True:
			process.interact()
		else:
			process.expect(["[#$]\s*", pexpect.EOF]) #COMMAND PROMPT or End of File for scp-like commands
	except pexpect.EOF:
		print "%sEncountered EOF while executing command \"%s\"%s" % (bcolors.WARNING, command, bcolors.ENDC)
	except pexpect.TIMEOUT:
		print "%sEncountered TIMEOUT while executing command \"%s\". No expected input received in this time%s\n\n" % (bcolors.FAIL, command, bcolors.ENDC)
		raise
	print "Result of executing \"%s\" is %s" %(command, process.before)	
