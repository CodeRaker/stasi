#!/usr/bin/env python3

import os

#change into git repo and pull
os.chdir(os.getcwd() + '/containers')
os.system('git pull')

#kill running process
os.system("kill $(ps -f | grep -m 1 direct_communicate_sidekick-sidekick.py | awk '{ printf $2 }')")

#build new image
os.system('python3 /projects/stasi/containers/direct_communicate_sidekick-sidekick.py &')
