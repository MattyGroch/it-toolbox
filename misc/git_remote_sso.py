import argparse
from misc.helper2 import Helper2
from misc.helper2 import get_script_name_from_python_file
import os

def run():
  parser = argparse.ArgumentParser(prog = get_script_name_from_python_file(__file__))
  parser.add_argument("-o", "--option")
  parser.add_argument("-f", "--flag", action="store_true")
  parser.add_argument("positional", nargs='?')
  <name>(parser.parse_args())

def <name>(args):
  git_scripts_repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  branch = Helper2(git_scripts_repo_path).current_branch()
  print("It works! Your local git-scripts repo is in branch '{0}'".format(branch))
  print("Run `python -m unittest test.{0}` to run the test".format('<name>'))
  return True

if __name__ == "__main__":
  run()

# display_help () {
#     echo "Usage: $0 [option]" >&2
#     echo
#     echo "   -e, --enable               Change remote CLI to use HTTPS (compatible with SSO)"
#     echo "   -d, --disable              Change remote CLI to use SSH (incompatible with SSO)"
#     echo
#     exit 1
# }
#
# enable_sso () {
# 	git config --global url."https://git.heroku.com/".insteadOf git@heroku.com:
#   git config --global url."https://github.com/".insteadOf git@github.com:
#   git config --global url."https://".insteadOf git://
# 	echo "Global config changed to use HTTPS. You may enable SSO."
# }
#
# disable_sso () {
# 	git config --global --unset url.https://git.heroku.com/.insteadOf
#   git config --global --unset url.https://github.com/.insteadOf
#   git config --global --unset url.https://.insteadOf
# 	echo "Global config reverted to original settings. You may now disable SSO."
# }
#
# while :
# do
# 	case "$1" in
# 		-h | --help)
# 			display_help
# 			exit 0
# 			;;
# 		-e | --enable)
# 			enable_sso
# 			exit 0
# 			;;
# 		-d | --disable)
# 			disable_sso
# 			exit 0
# 			;;
# 		-*)
# 			echo "Error: Unknown option: $1" >&2
# 			exit 1
# 			;;
# 		*)
# 			echo >&2 "Invalid argument given. Use [-h] to get help."
# 			exit 1
# 			;;
# 	esac
# done
