import sys, re
import importlib
from bcolors import bcolors
from .komey_cache import get_from_cache, put_in_cache, remove_from_cache

cmd_map = {}
stop_no_match = False

def load_cmd_map(cmd_map_file):
	with open(cmd_map_file) as f:
		global cmd_map
		for line in f:
			if line.startswith("#") or not line.strip():
				continue
			ar = line.strip().split(" ")
			reg_str = re.compile(ar[0], re.I)
			module_str, func_str = ar[1].rsplit('.',1)
			module_imp = importlib.import_module(module_str)
			#print module_imp
			func_name = getattr(module_imp, func_str)
			reg_act=ar[1:]
			reg_act[0]=func_name
			cmd_map[reg_str] = tuple(reg_act)
			
def get_action_args(act_list):
	action_dict = {}
	for action in act_list:
		ac = action.split("=")
		act_key = ac[0]
		act_val = ac[1]
		action_dict[act_key] = act_val
	return action_dict	
		
	
def switch_case(line):
	#print "cmd_map is %s" % cmd_map
	for reg_str, reg_act in cmd_map.iteritems():
		match = reg_str.search(line.strip())
		#match = pat.match(line.strip())
		#print "match is %s" % match
		if match is not None:
			#print "Found a match"
			user_args = match.groupdict()
			action = reg_act[0]
			action_args = get_action_args(reg_act[1:])
			action(action_args, user_args)
			return True
	return False

def substitute_params(line):
	def re_sub(matchObj):
		return get_from_cache(matchObj.group(1), "")
		
	return re.sub("\\$\\{(?P<key>\S+)\\}", re_sub, line, flags=re.I)
	
def exec_command(input_file):
	files = get_from_cache('files', [])
	files.append(input_file)
	put_in_cache('files',files)	
	with open(input_file) as f:
		for line in f:
			if line.startswith("#") or not line.strip():
				continue
			try:
				line = line.strip()
				line = substitute_params(line)
				found = switch_case(line)
				if found:
					print "%s%s - OK%s" %(bcolors.OKGREEN, line, bcolors.ENDC) 
				else:
					if stop_no_match:
						print "%sERROR - No action found for \"%s\" and stop_on_no_match is set to True. Program will exit.%s" %(bcolors.FAIL, line,bcolors.ENDC)
						break
					print "%sWARNING - dont know what to do with \"%s\". Skipping...%s" %(bcolors.WARNING, line, bcolors.ENDC)	
			except Exception, e:
				print "%sFAIL - Exception while executing command %s\n%s%s" %(bcolors.FAIL,line,e,bcolors.ENDC)
				#raise
	files = get_from_cache('files', [])
	files.pop() if len(files) > 0 else None
	put_in_cache('files',files)
	exit_file = get_from_cache(input_file+'_exit_command')
	if exit_file is not None:
		remove_from_cache(input_file+'_exit_command')
		exec_command(exit_file)
							
					
def set_stop_no_match(val):
	global stop_no_match
	stop_no_match = val
		
