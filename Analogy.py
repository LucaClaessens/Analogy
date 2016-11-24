"""
Analogy main controller
"""

import subprocess
import argparse
import os
import sys

COMMAND_MAP = {'generate' : ['Network', 'python model_to_DB.py -c 10'],
               'pdfconvert' : ['text-processing-tools', 'python pdf_to_trainingdata.py'],
               'setup' : ['Network', 'python initialize_servers.py'],
               'train' : ['Network', 'th train.lua -gpu_backend opencl']}

argparser = argparse.ArgumentParser(description='This is the main controller for Analogy. \
    \n\aHere you can control all parts of the Publishing system.')

argparser.add_argument('command', choices=COMMAND_MAP.keys(), help="generate: generate new \
    entries from the network to be processed.\n\a pdfconvert: convert PDF files stored in 'text-processing-tools/data' \
    to a file useable for training the model.\n\a setup: set up the servers listening to communicate between the network \
    and the web apps running on the iPads.\n\a train: initialize training scheme with standard controls. (running on OpenCL backend)")

args = argparser.parse_args()

origWD = os.getcwd()
c_map = COMMAND_MAP[args.command]

def execute(command):
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), c_map[0]))
    subprocess.check_output(command, shell=True, universal_newlines = True)

execute(c_map[1])
