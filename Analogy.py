"""

ANALOGY : PLATFORM-MINDED PUBLISHING
LICENSED UNDER THE GPL 3.0 LICENSE

For more copyright and license info, please read the LICENSE.txt file


"""

from ConfigParser import SafeConfigParser
import subprocess
import argparse
import os
import sys

parser = SafeConfigParser()
parser.read('analogy_config.ini')

cpu_only = parser.get('sampling','cpu_only')
gpu = 0

if cpu_only is True :
	gpu = -1

def execute(command):
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), C_MAP[0]))
    subprocess.check_output(command, shell=True, universal_newlines=True)

#MAP ALL COMMANDS
COMMAND_MAP = {'pdfconvert' : ['text-processing-tools', 'python pdf_to_trainingdata.py'],
               'setup' : ['Network', 'python initialize_servers.py'],
               'train' : ['Network', 'th train.lua -gpu {} -gpu_backend {}'.format(gpu, parser.get('sampling','backend'))]}


#PARSE THE ARGUMENTS
ARGPARSER = argparse.ArgumentParser(description='This is the main controller for Analogy. \
    \n\aHere you can control all parts of the Publishing system.')

ARGPARSER.add_argument('command', choices=COMMAND_MAP.keys(), help="\n\a pdfconvert: \
	convert PDF files stored in 'text-processing-tools/data' \
    to a file useable for training the model.\n\a setup: set up the servers listening to communicate between the network \
    and the web apps running on the iPads.")

ARGS = ARGPARSER.parse_args()

ORIGWD = os.getcwd()
C_MAP = COMMAND_MAP[ARGS.command]

#EXECUTE THE CHOSEN COMMAND
execute(C_MAP[1])
