#!/bin/bash

tar -c ./* | ssh azathoth@$1 "tar -x -C /home/azathoth/azathoth-server"
