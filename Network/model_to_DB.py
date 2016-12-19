import random
import subprocess
import MySQLdb
import atexit
import argparse

START_VAL = 1.0
iterations = 0
DEFAULT_CYCLES = 10
backend = 'opencl'

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser(description='How many cycles should we run?')
parser.add_argument("-c", "--cycles", type=check_positive, default=DEFAULT_CYCLES,
                    help="The number of sentences to create")

args = parser.parse_args()
max_iterations = args.cycles

db = MySQLdb.connect(
	unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
    host = 'localhost', 
    user = 'root', 
    passwd = 'root', 
    db = 'Analogy')

cursor = db.cursor()
db.escape_string("'")
db.escape_string('"')

def exit_handler():
	db.commit()
	db.close()
	print "done, lines committed to database."

atexit.register(exit_handler)

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

def upcase_first_letter(s):
    return s[0].upper() + s[1:]

def commit(sql):
	try:
		cursor.execute(sql)
		global iterations, max_iterations
		iterations += 1
		print "\n"
		print "committed, iteration {}".format(iterations)
		print "sql value was: {}".format(sql)
		print "\n"
		if iterations < max_iterations: generate_sentence()
		else: return None
	except (MySQLdb.Error, MySQLdb.Warning, TypeError) as e:
  		db.rollback()
  		print(e)
  		return None

def commit_to_db(sentence):
	sql_string = """INSERT INTO source_material (sentence_data, score, active, inserted_at)
    VALUES ("{}" , {}, TRUE , NULL);"""
	sql_insert = sql_string.format(sentence, START_VAL)
	commit(sql_insert)

def drop_sentence():
	print "dropped attempt to generate"
	return generate_sentence()

def generate_sentence():
	global backend
	prime = random_line().replace("\00", "")
	temp = "%.2f" % random.uniform(0.5, 0.95)
	length = random.randint(150,300)+len(prime)
	seed = random.randint(1000,9999)
	if temp > 0.1:
		command_string ='th sample.lua -gpu_backend {} -length {} -temperature {} -start_text "{}" -sample {}'
		command = command_string.format(backend, length, temp, prime, seed)
		returnvalue = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
		val = returnvalue.rsplit(prime)

		if len(val) >= 2 and val[1].strip():
			returnvalue = returnvalue.rsplit(prime)[1].split('.')[0]
		else: return drop_sentence()

		if returnvalue and returnvalue.strip():
			words = returnvalue.split(" ")
		else: return drop_sentence()

		if len(returnvalue) > 50:	
			if len(words[0]) < 3 or words[0].isdigit(): del words[0]
			badWords = ['the','any','of','and','a','as','to','1','in','by']
			while words[-1] in badWords or words[-1].endswith('\t\n'):
				words = words[0:-1]
			returnvalue = upcase_first_letter(" ".join(words)+".")
			print returnvalue
			print "\n"
			commit_to_db(returnvalue)
		else: return drop_sentence()
	else: return drop_sentence()

generate_sentence()