#!/usr/bin/env bash

display_help () {
    echo "Usage: $0 [option]" >&2
    echo
    echo "   -e, --enable               Change remote CLI to use HTTPS (compatible with SSO)"
    echo "   -d, --disable              Change remote CLI to use SSH (incompatible with SSO)"
    echo
    exit 1
}

enable_sso () {
	git config --global url."https://git.heroku.com/".insteadOf git@heroku.com:
  git config --global url."https://github.com/".insteadOf git@github.com:
  git config --global url."https://".insteadOf git://
	echo "Global config changed to use HTTPS. You may enable SSO."
}

disable_sso () {
	git config --global --unset url.https://git.heroku.com/.insteadOf
  git config --global --unset url.https://github.com/.insteadOf
  git config --global --unset url.https://.insteadOf
	echo "Global config reverted to original settings. You may now disable SSO."
}

while :
do
	case "$1" in
		-h | --help)
			display_help
			exit 0
			;;
		-e | --enable)
			enable_sso
			exit 0
			;;
		-d | --disable)
			disable_sso
			exit 0
			;;
		-*)
			echo "Error: Unknown option: $1" >&2
			exit 1
			;;
		*)
			echo >&2 "Invalid argument given. Use [-h] to get help."
			exit 1
			;;
	esac
done
