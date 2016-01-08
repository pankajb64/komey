def ssh_exec(command, terminal, interact):
	print "Execute over ssh - %s" % command
	terminal.sendline(command)
	if interact == True:
		terminal.interact()
	else:	
		terminal.prompt()
	print "Result of execution of %s is %s " % (command, terminal.before)

def ssh_exec_expect(command, expect, terminal, interact):
	count = expect['count']
	terminal.sendline(command)
	print "expect dict is %s" % expect
	try:
		for i in xrange(count):
			index = terminal.expect(expect['expect_list'])
			print "index is is %s expect is %s before is \n%s" %(index, expect['expect_list'][index], terminal.before)
			terminal.sendline(expect['response_list'][index])
		if interact == True:
			terminal.interact()
		#else:	
		#	terminal.prompt()
	except pexpect.EOF:
		print "%sEncountered EOF while executing command \"%s\"%s" % (bcolors.WARNING, command, bcolors.ENDC)
	except pexpect.TIMEOUT:
		print "%sEncountered TIMEOUT while executing command \"%s\". No expected input received in this time%s\n\n" % (bcolors.FAIL, command, bcolors.ENDC)
		raise
	print "Result of execution of %s is %s" % (command, terminal.before)
