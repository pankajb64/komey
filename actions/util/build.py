from actions.action_exec.action_exec import exec_command
import json
import requests
import xmltodict
import os

def ant_build(action_args, user_args):
	module_str = user_args['modules']
	modules = module_str.strip().split(",")
	for module in modules:
		command_args = { "module" : module }
		user_args['command_args'] = json.dumps(command_args)
		user_args['command_file'] = "base/ant_build"
		exec_command(action_args, user_args)

def take_backup(action_args, user_args):
	module = user_args.get('module')
	module = module.strip() if module is not None else ""
	hosts = user_args['hosts'].strip().split(",")
	cred = user_args['credentials'].strip()
	for host in hosts:
		command_args = { "backup_host" : host.strip(), "backup_cred" : cred, "backup_module" : module }
		print command_args
		user_args["command_args"] = json.dumps(command_args)
		user_args["command_file"] = "base/take_backup"
		exec_command(action_args, user_args)


def take_backup_base(action_args, user_args):
	#print "yaha aya"
	module = user_args.get('module', '').strip()
	command_args = {"backup_module" : module }
	user_args["command_args"] = json.dumps(command_args)
	user_args["command_file"] = "base/take_backup_base"
	exec_command(action_args, user_args)


def build_deploy_service(action_args, user_args):
	modules = user_args["modules"].strip().split(",")
	host = user_args["host"].strip()
	env = user_args["env"].strip()
	xml_file = os.getcwd() + '/data/config/' + env + '.xml'
	dicti = {}
	services = []
	actions = []
	with open(xml_file) as f:
		dicti = xmltodict.parse(f.read())
	ip_list = dicti["project"]["servicesmapped"]["ip"]
	print modules
	for elem in modules:
		ar = elem.split("-")
		module = ar[0].strip()
		mod_ip = ar[1].strip()
		for ip in ip_list:
			#print "mod_ip is %s ip value is %s equal? %s" %(mod_ip, ip["@value"], mod_ip == ip["@value"])
			if mod_ip == ip["@value"] or mod_ip == ip["@internalip"]:
				if type(ip["service"]) is list:
					for service in ip["service"]:
						print "service is %s module is %s equal? %s" % (service, module, service == module)
						if service == module:
							s = ip["@value"]+'-'+ip["@internalip"]+','+module.strip()
							services.append(s)
							actions.append(s+',build')
							if user_args.get("deploy") is not None:
								actions.append(s+',deploy')
				else:
					if ip["service"] == module:
						s = ip["@value"]+'-'+ip["@internalip"]+','+module.strip()
						services.append(s)
						actions.append(s+',build')
						if user_args.get("deploy") is not None:
							actions.append(s+',deploy')				
	print services
	print actions
	build_tool_url = "http://"+host+"/bms/dashsubmit.do"
	params = { 'services' : services, 'actions' : actions }
	result = requests.post(build_tool_url, data = params)
	print "Request executed. Result is %s" %result.text
