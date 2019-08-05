#!/bin/bash

display_help () {
    echo "Usage: $0 [option]" >&2
    echo
    echo "   -e, --enable               Change Heroku CLI to use HTTPS (compatible with SSO)"
    echo "   -d, --disable              Change Heroku CLI to use SSH (incompatible with SSO)"
    echo
    exit 1
}

enable_sso () {
	git config --global url."https://git.heroku.com/".insteadOf "git@heroku.com:"
	echo "Heroku configured for HTTPS. You may enable SSO."
}

disable_sso () {
	git config --global --unset url.https://git.heroku.com/.insteadOf
	echo "Heroku configured for SSH. You may now disable SSO."
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
			break
			echo >&2 "Invalid argument given. Use [-h] to get help."
			exit 1
			;;
	esac
done