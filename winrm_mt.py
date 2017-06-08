#!/usr/bin/python

import sys
import os
import getopt
import threading
import time
import subprocess
from winrm import Protocol

def parse_args():
        password = None
	environment = None
	action = None
	version = None
	cmd = None
	log = None
	server = None

        try:
            	opts, args = getopt.getopt(sys.argv[1:], "s:p:a:c:e:v:l:")
            	for opt, arg in opts:
                	if opt == "-s":
                    		server = arg
			elif opt == "-e":
		    		environment = arg
			elif opt == "-v":
		    		version = arg
                	elif opt == "-p":
                    		password = arg
                	elif opt == "-a":
                    		action = arg
			elif opt == "-c":
		    		cmd = arg

        except getopt.GetoptError:
            	print ("%s whatever args i want" %  sys.argv[0])
        return (server, password, environment, action, version, cmd)

class winrmThread (threading.Thread):
	def __init__(self, threadName, server, password, cmd, argList ):
      		threading.Thread.__init__(self)
		self.threadName = threadName
      		self.server = server
		self.cmd = cmd
		self.argList = argList
		self.password = password

   	def run(self):
                exit_code = 0
                protocol = "http"
                port = "5985"
                transport = "ntlm"
		username = r'mycompany.com\jenkins_user'
                endpoint = "%s://%s:%s/wsman" % (protocol, self.server , port)

      		print "###################Starting Task: %s" % (self.threadName)

		c = Protocol(endpoint=endpoint, transport=transport, username=username, password=self.password, server_cert_validation='ignore')
		shell_id = c.open_shell()
		command_id = c.run_command(shell_id, self.cmd, self.argList )
        	stdout, stderr, status_code = c.get_command_output(shell_id, command_id)
        	c.cleanup_command(shell_id, command_id)

		c.close_shell(shell_id)
      		print "###################Exiting Task: %s" % (self.threadName)

class tdThread (threading.Thread):
	def __init__(self, threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName

	def run(self):
      		print "###################Starting Task: %s" % (self.threadName)
                p = subprocess.Popen(['tail','-F', '/var/log/zdtsw.log'],stdout=subprocess.PIPE)
                while True:
                    line = p.stdout.readline()
                    print line.rstrip()
                    if line.rstrip() == 'Job finished':
                        break
                p.kill()
      		print "###################Exiting Task: %s" % (self.threadName)


def main():
	server, password, environment, action, version, cmd  = parse_args()

	# Create new threads:for start bat
	trdBatch = winrmThread(action, server, password, cmd, [environment, action, version])
        trTailLog = tdThread("Logging")

	# Start new Threads
	trdBatch.start()
	time.sleep(5)
	trTailLog.start()

        # Wait till both done
	trdBatch.join()
	trTailLog.join()


if __name__ == "__main__":
        main()
