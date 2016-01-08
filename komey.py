import sys
from actions.komey_util.komey_util import load_cmd_map, exec_command, set_stop_no_match

def main():
	input_file = sys.argv[1]
	stop_no_match = True if len(sys.argv) > 2 and sys.argv[2].strip().lower() == 'true' else False
	set_stop_no_match(stop_no_match)

	cmd_map_file = "command_mapping"
	load_cmd_map(cmd_map_file)

	exec_command(input_file)

if __name__ == "__main__":
	main()
