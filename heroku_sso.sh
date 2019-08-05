#!/bin/bash

if [[ -z "$@" ]]; then
    echo >&2 "You must supply an argument!"
    exit 1
fi

enable()
{
	git config --global url."https://git.heroku.com/".insteadOf "git@heroku.com:"
	exit 0
}

disable()
{
	git config --global --unset url.https://git.heroku.com/.insteadOf
	exit 0
}