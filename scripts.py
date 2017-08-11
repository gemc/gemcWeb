import os, hashlib, json, subprocess, time, shutil

basedir = os.path.abspath(os.path.dirname(__file__))

salt = "salty" #Generate a salt for security, do not use 'salty'

"""
To generate a salt run CL Python and run the following:

>>> import random
>>> ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(32))

Copy and paste this as your salt
"""

def create_account(user, password):
	"""Checks for new account validity. If valid, creates account"""
	if os.path.isdir(basedir + '/users/' + user):
		return False
	else:
		#hashing and salting the password
		global salt
		password = password + salt
		hash_object = hashlib.sha256(password)
		hex_dig = hash_object.hexdigest()
		#creating user directory and storing pasword
		os.mkdir(basedir + '/users/' + user)
		os.chdir(basedir+ '/users/' + user)
		with open ('pwd.txt' , 'w') as f:
			f.write(hex_dig + '\n')
		os.mkdir('projects')
		make_libs()
		return True

def make_libs():
	"""Makes user libraries"""
	os.mkdir('libs')
	os.chdir('libs')
	os.mkdir('mc')
	os.mkdir('gcards')
	os.mkdir('results')

def account_exists(user):
	"""Checks if user account exists"""
	if os.path.isdir(basedir + '/users/' + user):
		return True
	else:
		return False

def check_password(password):
	"""Returns a hashed version of password for log in check"""
	global salt
	password = password + salt
	hash_object = hashlib.sha256(password)
	hex_dig = hash_object.hexdigest()
	return hex_dig

def get_password(user):
	"""Gets hashed user password from pwd file"""
	os.chdir(basedir + '/users/' + user)
	with open('pwd.txt', 'r') as f:
		password = f.readline().strip()
	return password

def get_user_projects(user):
	"""Gets user projects and abstract to display on homepage"""
	projects = os.listdir(basedir + '/users/' + user +'/projects')
	dlst = []
	for p in reversed(projects):
		abstract = get_experiment_data(user, p, 'abstract')
		if abstract is "Empty Project":
			abstract = "Empty Project"
		elif abstract is "None specified":
			abtract = "None specified"
		else:
			abstract = str(abstract)[:40]
		d = {"title" : p, "abstract" : abstract}
		dlst.append(d)
	return dlst

def get_experiment_list():
	"""Gets the experiment list for new experiment template"""
	possible_experiments = []
	exp_dir = basedir + '/components/expjson'
	for exp in os.listdir(exp_dir):
		if exp.endswith('.json'):
			possible_experiments.append(exp[:-5])
	return possible_experiments

def create_project_dir(user, experiment):
	"""Creates a directory for an experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/')
	os.mkdir(experiment)

def create_experiment_data(user, experiment):
	"""Creates the data file for specific experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)
	create = 'created: ' + time.strftime('%d/%m/%Y') + '\n'
	gcard = 'gcard: ' + basedir + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.gcard\n'
	results = 'results: ' + basedir + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.ev\n'
	with open(experiment + '_data.txt', 'w+') as f:
		f.write(str(create))
		f.write(str(gcard))
		f.write(str(results))

def rename_project_dir(user, experiment, title):
	os.chdir(basedir + '/users/' + user + '/projects')
	count = 1
	while True:
		if os.path.exists(title):
			title = title + str(count)
			count = int(count) + 1
		else:
			break
	os.rename(experiment, title)
	os.chdir(title)
	os.rename(experiment + '_data.txt', title + '_data.txt')
	oldgcard = 'gcard: ' + basedir + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.gcard\n'
	oldresults = 'results: ' + basedir + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.ev\n'
	gcard = 'gcard: ' + basedir + '/users/' + user + 'projects/' + title + '/' + title + '.gcard\n'
	results = 'results: ' + basedir + '/users/' + user + 'projects/' + title + '/' + title + '.ev\n'

	f = open(title + '_data.txt', 'r')
	lines = f.readlines()
	f.close

	f = open(title + '_data.txt' ,'w')
	f.write(str(gcard))
	f.write(str(results))
	for line in lines:
		if line == oldgcard:
			pass
		elif line == oldresults:
			pass
		else:
			f.write(line)
	f.close()
	return title

def clone_project(user, experiment):
	"""Clone project, same as edit, but keeps original project files"""
	os.chdir(basedir + '/users/' + user + '/projects')

	count = 1
	clone_title = experiment + '_clone' + str(count)

	while True:
		if os.path.exists(title):
			clone_title = title + str(count)
			count = int(count) + 1
		else:
			break

	shutil.copy(experiment, clone_title)

def write_experiment_data(user, experiment, part, content):
	"""Writes to data file for specific experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)
	l = str(part) + ': ' + str(content)
	l = str(l) + '\n'

	f = open(experiment + '_data.txt', 'r')
	lines = f.readlines()
	f.close

	f = open(experiment + '_data.txt' ,'w')
	for line in lines:
		if line.startswith(part):
			pass
		else:
			f.write(line)
	f.write(str(l))
	f.close()

def get_experiment_data(user, experiment, part):
	"""Gets part of data file for specific experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)
	if not(os.path.exists(experiment + '_data.txt')):
		return "Empty Project"
	else:
		with open(experiment + '_data.txt' , 'r') as f:
			lines = [x.strip('\n') for x in f.readlines()]
			for l in lines:
				if l.startswith(str(part)):
					index = len(part) + 2
					return l[index:]
		return "None specified" #Nothing code

def trim_ec(e):
	"""Gets the user's experiment choice in usable form"""
	delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
	e = str(e)
	e = e.translate(None, delchars)
	return e

def get_ec_info(e, part):
	"""Gets the experiment desctiption for user ec"""
	with open(basedir + '/components/expjson/' + e + '.json') as data_file:
		stock_json = json.load(data_file)
		return (stock_json[part])

def trim_ao(a):
	"""Gets the user's advanced options selections in uable form"""
	chars = ['[', ']', '"' ,',']
	for ch in chars:
		a = a.replace(ch,"")
	print a
	return a

def gen_gcard(user, experiment):
	"""Generates the gcard for new experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)

	user_gcard = experiment + '.gcard'
	user_out = experiment + '.ev'
	ec = None
	ao_list = None
	gl = None

	with open(experiment + '_data.txt','r') as f:
		lines = [x.strip('\n') for x in f.readlines()]
		for l in lines:
			if l.startswith('ec'):
				ec = l[4:]
			if l.startswith('ao'):
				a = l[4:]
				ao_list = a.split()
			if l.startswith('gl') :
				gl = l[4:]

	with open(basedir + '/components/expjson/' + ec + '.json') as data_file:
		stock_json = json.load(data_file)
		relevant_detectors = stock_json['detectors']

	if not(ao_list is None): #writing actual gcard, sees if ao used or not
		fo = open(user_gcard, "wb")
		fo.write("<gcard>" + '\n')
		for d in relevant_detectors:
			if d["name"] in ao_list:
				fo.write(d["tag"] + '\n')
			else:
				pass
		fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ gl +"'/>" + '\n')
		fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
		fo.write("</gcard>" + '\n')
		fo.close()
	else:
		fo = open(user_gcard, "wb")
		fo.write("<gcard>" + '\n')
		for d in relevant_detectors:
			print(d)
			fo.write(d["tag"] + '\n')
		fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ gl +"'/>" + '\n')
		fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
		fo.write("</gcard>" + '\n')
		fo.close()


def run_gemc(user,experiment):
	"""runs gemc"""
	import signal
	os.chdir(basedir + '/users/' + user + '/projects/' + experiment) #change to correct dir
	user_gcard = experiment + '.gcard'

	#copy over gcard to libraries
	gcard_dir = basedir + '/users/' + user + '/libs/gcards/'
	shutil.copy(user_gcard, gcard_dir)

	with open(experiment + '_out.txt', 'w+') as out: #running process
		p = subprocess.Popen(args=['/bin/csh', '-c', "gemc " +  user_gcard + " -USE_GUI=0"], stdout=out)

		child_pid = p.pid

		while 1:
			where = out.tell()
			line = out.readline()
			if not line:
				time.sleep(1)
				out.seek(where)
			else:
				if "Total gemc time:" in line:
					print line
					#kill gemc and close experiment_out.txt
					os.kill(child_pid, signal.SIGTERM)
					out.close()
					#copy over results to libraries
					res_dir = basedir + '/users/' + user + '/libs/results/'
					shutil.copy(out, res_dir)
					#return True for success
					return True
				elif "Abort" in line:
					print line
					#kill gemc and close experimemt_out.txt
					os.kill(child_pid, signal.SIGTERM)
					out.close()
					#return False for failure:
					return False
				else:
					pass
