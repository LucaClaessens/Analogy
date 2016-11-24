import random
import subprocess
import linecache

_ln = 0

lines = [
'This problematic contradiction is rarely discussed and the notion that blockchain is somehow radical, anti- authoritarian or alternative is leading a generation of creatives down a gloomy path.',
'The popular and contagious anti-authoritarian attitude is guiding our activists, programmers, artists, designers and businesses towards a common universal view that.',
'This unfortunately is not happening often enough and many initiatives quickly integrate blockchain technology without examining how the code will enforce a libertarian metricocratic reward system rather than offer sustainable solutions to economic inequality and consequently end up just expanding an unregulated network formatted towards hyper capital that will burn a hole in both your pocket and the planet.',
'The unfortunate twist is that eventually, once smart contracts are eventually embedded into IoT and turn all objects into autonomous economic agents, the hackers and designers will have contributed to an even greater surveillance state, that can utilize the infrastructure of connected devices to enforce and control society with self-executing open source code.',
'The diminishing ambition of engineering counter-cultures with technology stems from a broader failure witnessed in cyberculture from the early 90\'s to the turn of the millenia, to effectively produce a networked unregulated utopia beyond corporate or government control.'
'This is a radical moment: We are moving from the Euclidean economic space - a given, flat, rigid, non-changeable, zero-curvatured',
'We are about to start producing economic space itself. We are about to transform and terraform social, economic and financial structures of previous centuries.'
]

def upcase_first_letter(s):
	return s[0].upper() + s[1:]

def generate_sentence():
	global lines, _ln
	if not lines[_ln]: return None
	prime = lines[_ln].replace("\00", "")
	temp = "%.2f" % random.uniform(0.5, 0.95)
	length = random.randint(150,300)+len(prime)
	seed = random.randint(1000,9999);
	if temp > 0.1:
		command_string ='th sample.lua -gpu_backend opencl -length {} -temperature {} -start_text "{}" -sample {}'
		command = command_string.format(length, temp, prime, seed)
		returnvalue = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
		val = returnvalue.rsplit(prime)
		if len(val) >= 2 and val[1].strip():
			returnvalue = returnvalue.rsplit(prime)[1].split('.')[0]
		else: return generate_sentence()

		if returnvalue and returnvalue.strip():
			words = returnvalue.split(" ")
		else: return generate_sentence()

		if len(returnvalue) > 50:	
			if len(words[0]) < 3 or words[0].isdigit(): del words[0]
			badWords = ['the','any','of','and','a','as','to','1','in','by', '<is></is>']
			while words[-1] in badWords or words[-1].endswith('\t\n'):
				words = words[0:-1]
			returnvalue = upcase_first_letter(" ".join(words)+".")
			print returnvalue
			print "\n"
			_ln += 1
			generate_sentence()

		else: return generate_sentence()
	else: return generate_sentence()


generate_sentence()