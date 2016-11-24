"""
Analogy main controller
"""

import subprocess
import argparse
import os
import sys

COMMAND_MAP = {'generate' : ['Network', 'python model_to_DB.py -c 10'],
               'pdfconvert' : ['Content', 'python pdf_to_trainingdata.py'],
               'setup' : ['Network', 'python initialize_servers.py'],
               'train' : ['Network', 'th train.lua -gpu_backend opencl']}

argparser = argparse.ArgumentParser(description='This is the main controller for Analogy. \
    \nHere you can control all parts of the Publishing system.')

argparser.add_argument('command', choices=COMMAND_MAP.keys(), help="generate: generate new \
    entries from the network to be processed.\n pdfconvert: convert PDF files in 'Content/data' \
    to a file useable for training the model.")

args = argparser.parse_args()

origWD = os.getcwd()
c_map = COMMAND_MAP[args.command]

def execute2(command):
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), c_map[0]))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        print nextline
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if exitCode == 0:
        return output
    else:
        return 'fucked up'
        #raise ProcessException(command, exitCode, output)

def execute(command):
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), c_map[0]))
    subprocess.check_output(command, shell=True, universal_newlines = True)

execute(c_map[1])
