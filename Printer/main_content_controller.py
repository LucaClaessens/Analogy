from __future__ import print_function
from Publication_Maker import Publication_Maker 
from Adafruit_Thermal import *
from random import randrange
from PIL import Image
from ConfigParser import SafeConfigParser
import urllib, cStringIO , time
import sys


# Set configuration
parser = SafeConfigParser()
parser.read('../analogy_config.ini')

serial = parser.get('printer','use_serial')
serialport = parser.get('printer',serial)
baudrate = parser.get('printer','baudrate')

nextInterval = 0.0   # Time of next recurring operation

# Choose the right printer
printer      = Adafruit_Thermal(serialport, baudrate, timeout=5)
INTERVAL 	 = 5

def _init():
	global VERBOSE
	print('\n\n')
	print('***** ANALOGY *****')
	print('Welcome to the analogy print controller')
	if query_yes_no("Would you like to see verbose printing information?") is True:
		VERBOSE = True
	else:
		VERBOSE = False
	print('\n\n')
	_print()


# PRINTING HANDLER
def _print():
	global VERBOSE
	# sentences=[0],image=[1][0],type=[2]
	content = Publication_Maker(True, VERBOSE)

	# if the publication maker didn't get stuck
	if content != "stop" or None:
		# pipe the data to here
		data = content.output()

		#take some extra time to print premium
		if data[2] and data[1][0]: 
			output_print(data[0],data[1][0],data[2])
			INTERVAL = (content.update_interval() * 5000)
			time.sleep(10)
			prompt_new()
		else: 
			#take some time to print free
			output_print(data[0],data[1],data[2])
			INTERVAL = (content.update_interval() * 5000)
			time.sleep(2)
			prompt_new()
	else: 
		print("didn't print, something went wrong.") 

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# print the publication
def output_print(sentences,img_url,pubtype):
	if VERBOSE:	print(img_url)
	printer.feed(3)
	create_header(pubtype)
	printer.feed(1)
	if pubtype: #premium
		create_img(img_url, True)
		printer.feed(1)
	create_sentences(sentences,pubtype)
	printer.feed(3)

#prompt for a new print
def prompt_new():
	print('printing finished :)')
	if query_yes_no("Print another page?") is True:
		_init()
	else:
		print('thanks for using Analogy.')
		exit()

# print the header of the publication
def create_header(pubtype):
	printer.doubleHeightOn()
	printer.println('LABFEST')
	printer.doubleHeightOff()
	printer.feed(1)
	_str = time.strftime('%b %d %Y %H:%M:%S')
	printer.inverseOn()
	printer.println(_str)
	printer.inverseOff()
	return _str

# convert the image url to an image and print it
def create_img(url, remote):
	if remote: file = cStringIO.StringIO(urllib.urlopen(url).read())
	else: file = url
	img = Image.open(file)
	printer.printImage(img)

# form the sentences to be printed
def create_sentences(sentences,pubtype):
	 #keep track of amount of characters printed
	characters_written = 0
	i = 0
	p = 1
	
	for sentence in sentences:

		#special character issue patches.
		sentence = sentence.replace("\xe2\x80\x93", '-').replace("\xe2\x80\x98", "'").replace("\xe2\x80\x99", "'")

		characters_written += len(sentence)
		#start printing

		# free, add ads if less than 3 ads printed already
		if not pubtype and i > 0 and p < 3:
			# if printed over 1000 chars, stop printing
			if characters_written > 1000:
				break
			advert = randrange(0,10) > 7
			# print advert if returns true
			if (advert):
				printer.feed(2)
				path = 'ads/Ad_{}.jpg'.format(randrange(1,4))
				create_img(path, False);
				printer.feed(2)

		# make line end with '.'
		if not sentence.endswith('.'): sentence += "."
		printer.println(sentence)
		printer.feed(2)
		i += 1

	# add a little footer to premium prints
	if pubtype: 
		printer.feed(1)
		printer.justify('C')
		printer.println("-------------------")
		printer.println("Thank you for contributing")
		printer.feed(2)
		printer.doubleHeightOn()
		printer.println('ANALOGY')
		printer.doubleHeightOff()
		printer.justify('L')
		printer.feed(1)

#Start
_init()