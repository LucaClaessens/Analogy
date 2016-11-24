from __future__ import print_function
from Publication_Maker import Publication_Maker 
from Adafruit_Thermal import *
from random import randrange
from PIL import Image
import urllib, cStringIO , time, threading

nextInterval = 0.0   # Time of next recurring operation
printer      = Adafruit_Thermal("/dev/tty.usbserial", 9600, timeout=5)
#printer     = Adafruit_Thermal("/dev/ttyAMA0", 9600, timeout=5)
#UNCOMMENT PREV LINE IF USING STRAIGHT FROM RASPI
INTERVAL = 30


def _init():
	# sentences[0],image[1],type[2]
	content = Publication_Maker(True)
	if content != "stop" or None:
		data = content.output()
		print("ran init");
		#if data[2]: output_print(data[0],data[1][0],data[2])
		#else: output_print(data[0],data[1],data[2])
	else:
		print("didn't update")
	#update interval between runs based on print count and balance
	INTERVAL = (content.update_interval() * 30)
	#run script again after specified time
	threading.Timer(INTERVAL, _init).start()

def output_print(sentences,img_url,pubtype):
	print(img_url)
	printer.feed(3)
	create_header(pubtype)
	printer.feed(1)
	if pubtype: #premium
		create_img(img_url, True)
		printer.feed(1)
	create_sentences(sentences,pubtype)
	printer.feed(3)
	print('printing finished :)')


def create_header(pubtype):
	printer.doubleHeightOn()
	printer.println('MONEYLAB #3')
	printer.doubleHeightOff()
	printer.feed(1)
	_str = time.strftime('%b %d %Y %H:%M:%S')
	printer.inverseOn()
	printer.println(_str)
	printer.inverseOff()
	return _str

def create_img(url, remote):
	if remote: file = cStringIO.StringIO(urllib.urlopen(url).read())
	else: file = url
	img = Image.open(file)
	printer.printImage(img)

def create_sentences(sentences,pubtype):
	 #keep track of amount of characters printed
	characters_written = 0
	i = 0
	p = 1
	for sentence in sentences:
		characters_written += len(sentence)
		if not pubtype and i > 0 and p < 3: # not premium
			if characters_written > 1000:
				break
			advert = randrange(0,10) > 7
			if (advert):
				printer.feed(2)
				#no = str(randrange(1,2));
				path = 'ads/Ad_{}.jpg'.format(randrange(1,4))
				create_img(path, False);
				printer.feed(2)
		if not sentence.endswith('.'): sentence += "."
		printer.println(sentence)
		printer.feed(2)
		i += 1


_init()