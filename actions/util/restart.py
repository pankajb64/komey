from actions.action_exec.action_exec import exec_command
from actions.ssh.ssh import ssh_login, ssh_logout
import json
import os

def restart_tomcat(action_args, user_args):
	hosts = user_args['hosts'].strip().split(",")
	cred = user_args['credentials'].strip()
	for host in hosts:
		command_args = { "restart_tomcat_host" : host.strip(), "restart_tomcat_cred" : cred }
		user_args["command_args"] = json.dumps(command_args)
		user_args["command_file"] = "base/restart_tomcat"
		exec_command(action_args, user_args)

def restart_tomcat_base(action_args, user_args):
	user_args["command_args"] = "{}"
	user_args["command_file"] = "base/restart_tomcat_base"
	exec_command(action_args, user_args)


def restart_apache(action_args, user_args):
	hosts = user_args['hosts'].strip().split(",")
	cred = user_args['credentials'].strip()
	for host in hosts:
		command_args = { "restart_tomcat_host" : host.strip(), "restart_tomcat_cred" : cred }
		user_args["command_args"] = json.dumps(command_args)
		user_args["command_file"] = "base/restart_tomcat"
		exec_command(action_args, user_args)

def restart_tomcat_base(action_args, user_args):
	user_args["command_args"] = "{}"
	user_args["command_file"] = "base/restart_tomcat_base"
	exec_command(action_args, user_args)

def stop_service(action_args, user_args):
	modules = user_args["modules"].strip().split(",")
	hosts = user_args["hosts"].strip().split(",")
	cred = user_args["credentials"].strip()
	for host in hosts:
		host = host.strip()
		user_args["host"] = host
		user_args["nick"] = "stop_"+host
		credentials_file = os.getcwd() + '/data/credentials/' + user_args['credentials'].strip()
		credentials = {}
		with open(credentials_file) as f:
			credentials = json.load(f)
		ssh_login(action_args, user_args)
		for module in modules:
			command_args= { "mod_password" : credentials["password"], "module" : module}
			user_args["command_args"] = json.dumps(command_args)
			user_args["command_file"] = "base/stop_base"
			exec_command(action_args, user_args)
		ssh_logout(action_args, user_args)	

def start_service(action_args, user_args):
	modules = user_args["modules"].strip().split(",")
	hosts = user_args["hosts"].strip().split(",")
	cred = user_args["credentials"].strip()
	for host in hosts:
		host = host.strip()
		user_args["host"] = host
		user_args["nick"] = "start_"+host
		credentials_file = os.getcwd() + '/data/credentials/' + user_args['credentials'].strip()
		credentials = {}
		with open(credentials_file) as f:
			credentials = json.load(f)
		ssh_login(action_args, user_args)
		for module in modules:
			command_args= { "mod_password" : credentials["password"], "module" : module}
			user_args["command_args"] = json.dumps(command_args)
			user_args["command_file"] = "base/start_base"
			exec_command(action_args, user_args)
		ssh_logout(action_args, user_args)	
