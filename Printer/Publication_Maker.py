from __future__ import division
import socket, MySQLdb
from PIL import Image
from random import randint, randrange
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('../analogy_config.ini')

db = MySQLdb.connect(
    host = parser.get('database','host'), 
    user = parser.get('database','user'), 
    passwd = parser.get('database','passwd'), 
    db = parser.get('database','db'),
    port = 3306
	)

cursor = db.cursor()

# Set global printing variables
SBMAX 						= 1.5
SBMIN 						= 0.0
MIN_PRINT_BEFORE_BALANCE	= 10
BALANCE 					= 0.333
MIN_AVAIL 					= 8
MIN_POOL 					= 15


class Publication_Maker():

	#Set instanced printing variables
	FREE 					= 0 
	PUB 					= 0

	FREEPRINTED 			= 0
	PUBPRINTED 				= 0
	TOTALPRINTED 			= 0

	POOL 					= 0
	tier 					= None
	search_pattern 			= False
	pref_premium 			= False
	seeded 					= False
	locked		 			= False
	VERBOSE					= True

	def __init__(self,*args):

		#output variables have to be defined first
		self.is_premium 	= None
		self.selected_sentences = []
		self.selected_image = ""

		# (search_pattern, tier) = (True, 'premium')
		# search pattern defines if search based on existing material
		if len(args) == 0:
			print "Publication_Maker: please insert the arguments: \
				searchpattern: True/False **Mandatory\npreference: 'free'\'premium' **Optional"
			return None
		elif len(args) == 1:
			args = [ args[0], False ]
		else:
			args = [args[0], args[1]]

		if args[0] == True :
			self.analyze_content()
		else:
			self.pref_premium = False
			self.handle_formation()
		if args[1] == False:
			self.VERBOSE = False
		else:
			self.VERBOSE = True

		print "Attempting to print a publication."

	# Take a look at the amount of prints already produced and their distribution
	def update_print_count(self):

		_s = "SELECT COUNT(*) FROM prints;"
		self.TOTALPRINTED = self.return_sql_array(_s)[0]

		_s = "SELECT COUNT(*) FROM prints WHERE premium = TRUE;"
		self.PUBPRINTED = self.return_sql_array(_s)[0]

		self.FREEPRINTED = self.TOTALPRINTED - self.PUBPRINTED
		if self.VERBOSE:
			print('total prints: {}'.format(self.TOTALPRINTED))
			print('published prints: {}'.format(self.PUBPRINTED))

	# Analyze 
	def analyze_content(self):
		self.update_print_count()

		#read the scores of all the entries in the source material
		_s = "SELECT score FROM source_material" 
		result = self.return_sql_array(_s)

		# divide the scores into categories
		for score in result:

			if score < SBMIN: self.FREE+=1
			elif score > SBMAX: self.PUB+=1
			else : self.POOL+=1

		# see if there's enough data to continue
		if self.POOL < MIN_POOL:
			print 'Need a bigger datapool, wait until someone interacts with the iPad setup or call the analogy.py script.'
			return None 
		else:

			# can we work with balance yet?
			if self.TOTALPRINTED > MIN_PRINT_BEFORE_BALANCE:
				CURRENT_BALANCE = self.PUBPRINTED / self.FREEPRINTED
				if self.VERBOSE:
					print 'Free items available:{}\nPublishable items available:{}\nItems in pool:{}\nBalance:{}\n'.format(self.FREE,self.PUB, self.POOL, CURRENT_BALANCE )
				
				# in case of lot of free content, print premium
				if CURRENT_BALANCE < BALANCE:
					 _s = "SELECT COUNT(sentence_data) FROM source_material WHERE score > {}".format(SBMAX);
					 self.pref_premium = True
				#otherwise print free content
				else : 
					_s = "SELECT COUNT(sentence_data) FROM source_material WHERE score < {}".format(SBMIN);
					self.pref_premium = False

				quantity = self.return_sql_array(_s)[0]

				# if there's enough data available to print a new piece of paper, handle forming it
				if quantity > MIN_AVAIL:
					self.handle_formation()
				# otherwise lock the script, this will later on prevent printing
				else:
					self.locked = True
					return False
			
			#if we can't work with balance, but there's enough data, go ahead and print something random
			else:
				print 'Need more prints to work with balance, will attempt to print random type of publication.'
				self.pref_premium = randrange(100) < 50
				if self.pref_premium == True:
					_s = "SELECT COUNT(sentence_data) FROM source_material WHERE score > {}".format(SBMAX);
				else:
					_s = "SELECT COUNT(sentence_data) FROM source_material WHERE score < {}".format(SBMIN);
				quantity = self.return_sql_array(_s)[0]
				if quantity > MIN_AVAIL:
					self.handle_formation(self.pref_premium)
				else:
					self.locked = True
					return False

	# Update when to print again
	def update_interval(self):
		return abs(BALANCE / ( self.PUBPRINTED - self.FREEPRINTED ));

	# Read from the database
	def return_sql_array(self, _s):
		try:
			cursor.execute(_s)
			data=cursor.fetchall()
			if len(data) == 0:
				return False
			else:
				_a = []
				for row in data:
					_a.append(row[0])
				return _a
		except (MySQLdb.Error, MySQLdb.Warning, TypeError) as e:
  			return e

  	# Write to the database
  	def write_sql(self, _s):
  		cursor.execute(_s)
  		return None

  	# generates a seed to try and find image/text matches with
	def find_seed(self):
		# WEIGHTING BUG -> SEEDING WITH SAME NUMBER SO WEIGHT HAS NO EFFECT
		#JUST RANDOMLY LOOP FOR HITS, SEEMS TO WORK BETTER.

		_s = """SELECT selected_data FROM selected_text WHERE score > 0 AND selected_length < 15
		ORDER by RAND() ASC LIMIT 5"""
		cursor.execute(_s)
		data=cursor.fetchall()
		str_array = []

		# load the chosen words into a list
		for row in data:
			_p = row[0].split( )
			str_array.extend(_p)

		# try to find a matching image with the words in the list
		for list_item in str_array:
			_s = """SELECT image_id FROM images WHERE image_key= "{}" AND key_score >= 1""".format(list_item)
			return [list_item, self.return_sql_array(_s)]

	# request text graded for premium publications
	def create_premium_text(self,seed):	
		_s = """SELECT `selected_data` , MATCH `selected_data` AGAINST ('{}') AS relevance FROM selected_text ORDER BY relevance DESC LIMIT 10""".format(seed);
		result = self.return_sql_array(_s)
		if self.VERBOSE:
			print 'premium text items found: {} for seed: {}'.format(len(result), seed)
		return result

	# try to link images
	def link_image(self,seed):
		_s = """SELECT image_url FROM images WHERE image_key = "{}"
		ORDER by key_score DESC LIMIT 1"""
		_s = _s.format(seed)
		result = self.return_sql_array(_s)
		return result
	
	def commit(self):
		db.commit()
		#db.close()

	#outputs the formed data to the controller script
	def output(self):
		if self.locked is True:
			self.commit()
			if self.pref_premium: t = 'premium' 
			else: t= 'free'
			return "Can't print a {} publication yet, waiting for more entries to print.".format(t)
		else:
			if self.is_premium: _v = 1
			else: _v = 0
			_s = "INSERT INTO prints (premium) values  ({})".format(_v);
			self.write_sql(_s)
			if self.VERBOSE:
				print self.selected_sentences
				print self.selected_image
				print self.is_premium
			return [self.selected_sentences, self.selected_image, self.is_premium]

	# handles the forming of the publication
	def handle_formation(self):

		# if it's a premium publication
		if self.pref_premium:
			i = 0

			#look for image/text relation if premium
			while not self.seeded:
				i+= 1
				seed = self.find_seed()
				if seed[1] != False : break
				# if didn't work in 250 tries break from the loop
				elif i > 250: 
					print "can't find a seed for the image linking sequence quick enough, try to run again." 
					return None

			print('seed: {}'.format(seed));

			#generate text and image needed for the publication
			self.selected_sentences = self.create_premium_text(seed[0])
			self.selected_image = self.link_image(seed[0])
			self.is_premium = True

		# if it's a free publication
		else: 
			_s = "SELECT sentence_data FROM source_material WHERE score < {} ORDER BY RAND() LIMIT 5".format(SBMIN)
			# just generate the text
			self.selected_sentences = self.return_sql_array(_s)