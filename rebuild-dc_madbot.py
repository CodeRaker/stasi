#!/usr/bin/env python3

import os

#cwd = os.getcwd()

#remove currect container and image
os.system('docker stop $(docker ps -a | grep dc_madbot | awk \'{ printf $1 }\')')
os.system('docker rm $(docker ps -a | grep dc_madbot | awk \'{ printf $1 }\')')
os.system('docker rmi $(docker images | grep dc_madbot | awk \'{ printf $3 }\')')

#change into git repo and pull
os.chdir(os.getcwd() + '/containers')
os.system('git pull')

#build new image
os.system('docker build -t dc_madbot:stasi -f direct_communicate_madbot-dockerfile .')

#start new container
os.system('docker run -d dc_madbot:stasi')
