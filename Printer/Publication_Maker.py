from __future__ import division
import socket, MySQLdb
from PIL import Image
from random import randint, randrange

#db = MySQLdb.connect(
#	unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
#	host = 'localhost',
#	user = 'root', 
#	passwd = 'root', 
#	db = 'Analogy')

db = MySQLdb.connect(
	host = 'luca.local',
	port = 3306,
	user = 'luca', 
	passwd = 'Analogy',
	db = 'Analogy')

cursor = db.cursor()

# Think of better way to distribute min/max values
SBMAX = 1.5
SBMIN = 0.0
MIN_PRINT_BEFORE_BALANCE = 10
BALANCE = 0.333
MIN_AVAIL = 8
MIN_POOL = 15


class Publication_Maker():

	FREE = 0 
	PUB = 0

	FREEPRINTED = 0
	PUBPRINTED = 0
	TOTALPRINTED = 0

	POOL = 0
	tier = None
	search_pattern = False
	pref_premium = False
	seeded = False
	locked = False

	def __init__(self,*args):

		#output variables have to be defined first
		self.is_premium = None
		self.selected_sentences = []
		self.selected_image = ""

		# (search_pattern, tier) = (True, 'premium')
		# search pattern defines if search based on existing material
		if len(args) == 0:
			print "Publication_Maker: please insert the arguments: \
				searchpattern: True/False **Mandatory\npreference: 'free'\'premium' **Optional"
			return None
		elif len(args) == 1:
			args = [ args[0], None ]
		else:
			args = [args[0], args[1]]

		if args[0] == True :
			self.analyze_content()
		else:
			self.pref_premium = False
			self.handle_formation()

	def update_print_count(self):
		_s = "SELECT COUNT(*) FROM prints;"
		self.TOTALPRINTED = self.return_sql_array(_s)[0]
		_s = "SELECT COUNT(*) FROM prints WHERE premium = TRUE;"
		self.PUBPRINTED = self.return_sql_array(_s)[0]
		self.FREEPRINTED = self.TOTALPRINTED - self.PUBPRINTED
		print(self.TOTALPRINTED)
		print(self.PUBPRINTED)

	def analyze_content(self):
		self.update_print_count()
		_s = "SELECT score FROM source_material" 
		result = self.return_sql_array(_s)
		for score in result:

			if score < SBMIN: self.FREE+=1
			elif score > SBMAX: self.PUB+=1
			else : self.POOL+=1

		if self.POOL < MIN_POOL:
			print 'Need a bigger datapool, wait until someone interacts with the iPad setup or call the analogy.py script.'
			return None 
		else:
			if self.TOTALPRINTED > MIN_PRINT_BEFORE_BALANCE:
				CURRENT_BALANCE = self.PUBPRINTED / self.FREEPRINTED
				print 'Free items available:{}\nPublishable items available:{}\nItems in pool:{}\nBalance:{}\n'.format(self.FREE,self.PUB, self.POOL, CURRENT_BALANCE )
				if CURRENT_BALANCE < BALANCE:
					 _s = "SELECT COUNT(sentence_data) FROM source_material WHERE score > {}".format(SBMAX);
					 self.pref_premium = True
				else : 
					_s = "SELECT COUNT(sentence_data) FROM source_material WHERE score < {}".format(SBMIN);
					self.pref_premium = False
				quantity = self.return_sql_array(_s)[0]
				if quantity > MIN_AVAIL:
					self.handle_formation()
				else:
					self.locked = True
					return False
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

	def update_interval(self):
		return abs(BALANCE / ( self.PUBPRINTED - self.FREEPRINTED ));

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
  			print(e)
  			return None

  	def write_sql(self, _s):
  		cursor.execute(_s)
  		return None

	def find_seed(self):
		_s = """SELECT selected_data, score, RAND() * score 
		AS weighted_score FROM selected_text WHERE score > 0 AND selected_length < 15
		ORDER by RAND() * weighted_score DESC LIMIT 5"""
		cursor.execute(_s)
		data=cursor.fetchall()
		str_array = []
		for row in data:
			_p = row[0].split( )
			str_array = str_array + _p

		for list_item in str_array:
			_s = """SELECT image_id FROM images WHERE image_key= "{}" AND key_score >= 1""".format(list_item)
			return [list_item, self.return_sql_array(_s)]

	def create_premium_text(self,seed):	
		_s = """SELECT `sentence_data` from source_material WHERE MATCH `sentence_data` AGAINST ("{}") LIMIT 10 """.format(seed);
		result = self.return_sql_array(_s)
		#print 'premium text item found: {}'.format(result)
		return result

	def link_image(self,seed):
		_s = """SELECT image_url FROM images WHERE image_key = "{}"
		ORDER by key_score DESC LIMIT 1"""
		_s = _s.format(seed)
		result = self.return_sql_array(_s)
		return result

	def handle_formation(self):
		if self.pref_premium:
			i = 0
			while not self.seeded:
				i+= 1
				seed = self.find_seed()
				if seed[1] != False : break
				elif i > 250: 
					print "can't find a seed quick enough, try to run again." 
					return None
			self.selected_sentences = self.create_premium_text(seed[0])
			self.selected_image = self.link_image(seed[0])
			self.is_premium = True
		else: 
			_s = "SELECT sentence_data FROM source_material WHERE score < {} ORDER BY RAND() LIMIT 5".format(SBMIN)
			self.selected_sentences = self.return_sql_array(_s)
		#print("I'm printing premium? {}\nSelected sentences array: {}".format(premium, self.selected_sentences))
	
	def commit(self):
		db.commit()
		db.close()

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
			self.commit()
			print self.selected_sentences
			print self.selected_image
			print self.is_premium
			return [self.selected_sentences, self.selected_image, self.is_premium]