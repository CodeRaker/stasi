#!/usr/bin/env python3

import os

#pull
os.system('git pull')

#kill running process
os.system("kill $(ps -f | grep -m 1 direct_communicate_madbot-madbot.py | awk '{ printf $2 }')")

#build new image
os.system('python3 /projects/stasi/containers/direct_communicate_madbot-madbot.py >> /projects/stasi/containers/direct_communicate_madbot-madbot.log 2>&1 &')
