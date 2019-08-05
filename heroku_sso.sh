#!/bin/bash

error () {
    echo >&2 "Missing parameter!"
    echo >&2 "[-up] to enable SSO support."
    echo >&2 "[-down] to disable SSO support."
    exit 1
}

enable () {
	git config --global url."https://git.heroku.com/".insteadOf "git@heroku.com:"
	echo "Heroku configured for HTTPS. You may enable SSO."
	exit 0
}

disable () {
	git config --global --unset url.https://git.heroku.com/.insteadOf
	echo "Heroku configured for SSH. You may now disable SSO."
	exit 0
}

if [ "$1" == "-up" ]; then
	enable
elif [ "$1" == "-down" ]; then
	disable
else
	error
fi
