#!/bin/bash

while getopts "t" opt; do
	case $opt in
		t) testmode=true
	esac
done

if [[ $testmode = true ]]; then
	socat PTY,link=$HOME/COM1 PTY,link=$HOME/COM2 &
	socat PTY,link=$HOME/COM3 PTY,link=$HOME/COM4 &
	twistd -n azathoth --io=$HOME/COM1 --drive=$HOME/COM3
	rm $HOME/COM*
else
	twistd -n azathoth
fi
