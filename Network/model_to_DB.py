import random
import subprocess
import MySQLdb
import atexit
from ConfigParser import SafeConfigParser

iterations = 0

## Load configuration
parser = SafeConfigParser()
parser.read('../analogy_config.ini')

START_VAL = parser.get('sampling','start_value')

backend = parser.get('sampling', 'backend')
checkpoint = parser.get('sampling', 'checkpoint')
max_iterations = parser.get('sampling','sample_cycles')
cpu_only = parser.get('sampling','cpu_only')
gpu = 0

# Set up DB connection
db = MySQLdb.connect(
	unix_socket = parser.get('database','unix_socket'),
    host = parser.get('database','host'), 
    user = parser.get('database','user'), 
    passwd = parser.get('database','passwd'), 
    db = parser.get('database','db')
    )

db.escape_string("'")
db.escape_string('"')

cursor = db.cursor()

# Code executed at shutdown, commit to the DB and close the connection
def exit_handler():
	db.commit()
	db.close()
	print "data committed to database."

atexit.register(exit_handler)


# Select a (semi)random line of text from the textfile with prime sentences
def random_line():
    line_num = 0
    selected_line = " "
    with open("primetext.txt", "rU") as f:
        while 1:
            line = f.readline()
            if not line: break
            line_num += 1
            if random.uniform(0, line_num) < 1:
                selected_line = line
    return selected_line.strip()

#uppercase the first letter of the string passed to the function
def upcase_first_letter(s):
    return s[0].upper() + s[1:]

#handler for committing the current iteration to the database
def commit(sql):
	try:
		cursor.execute(sql)
		global iterations, max_iterations
		iterations += 1
		print "\n"
		print "committed iteration no: {}".format(iterations)
		print "\n"
		if iterations < max_iterations: generate_sentence()
		else: return None
	except (MySQLdb.Error, MySQLdb.Warning, TypeError) as e:
  		db.rollback()
  		print(e)
  		return None

# Commit data to the db.
def commit_to_db(sentence):
	sql_string = """INSERT INTO source_material (sentence_data, score, active, inserted_at)
    VALUES ("{}" , {}, TRUE , NULL);"""
	sql_insert = sql_string.format(sentence, START_VAL)
	commit(sql_insert)

# Handles looping when generation attempt failed.
def drop_sentence():
	print "dropped attempt to generate"
	return generate_sentence()

# Main function, sample the network and clean up the output, see if it matches criteria set.
def generate_sentence():
	global backend, checkpoint, gpu

	# cut empty bytes out of the text, they cause errors.
	prime = random_line().replace("\00", "")
	# set the network temperature, handling the 'riskyness'
	temp = "%.2f" % random.uniform(0.5, 0.95)
	# choose a length for the text we want to be outputted
	length = random.randint(150,300)+len(prime)
	# set a seed for the network
	seed = random.randint(1000,9999)

	# if the temperature is too low the network will spit out garbage or do nothing at all
	if temp > 0.1:
		command_string ='th sample.lua -gpu {} -gpu_backend {} -length {} -temperature {} -start_text "{}" -sample {} -checkpoint {}'
		command = command_string.format(gpu, backend, length, temp, prime, seed, checkpoint)
		# pipe the command back from the subprocess, it's not advised to used 'shell=True'
		# due to security risks, yet I can't seem to find a way around this for now
		returnvalue = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
		# cut the returned value after the prime text, leaving us with the generated string
		val = returnvalue.rsplit(prime)
		print val;

		# test if the returned string contains newly generated text
		if len(val) >= 2 and val[1].strip():
			#if so, select the sentence
			returnvalue = returnvalue.rsplit(prime)[1].split('.')[0]
		else: return drop_sentence()

		# make sure we have a proper sentence
		if returnvalue and returnvalue.strip():
			words = returnvalue.split(" ")
		else: return drop_sentence()

		# if the sentence is over 50 characters
		if len(returnvalue) > 50:	
			# see if the first word has to be cut out
			if len(words[0]) < 3 or words[0].isdigit(): del words[0]
			badWords = parser.get('sampling','bad_end_words')

			# clip last word as long as it is part of our dictionary of bad words to end with
			# in case it isn't, continue and commit the value to the database
			while words[-1] in badWords.splitlines() or words[-1].endswith('\t\n'):
				words = words[0:-1]
			returnvalue = upcase_first_letter(" ".join(words)+".")
			print returnvalue
			print "\n"
			commit_to_db(returnvalue)
		else: return drop_sentence()
	else: return drop_sentence()

#see in what mode to sample from the network
if cpu_only is True :
	gpu = -1

#initialize the loop
generate_sentence()