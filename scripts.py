import os, hashlib, json, subprocess, time, shutil

basedir = os.path.abspath(os.path.dirname(__file__))

def create_account(user, password):
	"""Checks for new account validity. If valid, creates account"""
	if os.path.isdir(basedir + '/users/' + user):
		return False
	else:
		#hashing and salting the password
		hash_object = hashlib.sha256(password)
		hex_dig = hash_object.hexdigest()
		#creating user directory and storing pasword
		os.mkdir(basedir + '/users/' + user)
		os.chdir(basedir+ '/users/' + user)
		os.mkdir('projects')
		with open ('pwd.txt' , 'w') as f:
			f.write(hex_dig + '\n')
			return True

def account_exists(user):
	"""Checks if user account exists"""
	if os.path.isdir(basedir + '/users/' + user):
		return True
	else:
		return False

def check_password(password):
	"""Returns a hashed version of password for log in check"""
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
		if abstract == -1:
			abstract = "~empty project~"
		elif abstract is "Nada":
			abtract = "None found"
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
	gcard = 'gcard: ' + basedir + '/users/' + user + 'projects/' + experiment + '/g.gcard\n'
	results = 'results: ' + basedir + '/users/' + user + 'projects/' + experiment + '/r.ev\n'
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
	return title

def write_experiment_data(user, experiment, part, content):
	"""Writes to data file for specific experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)
	l = str(part) + ': ' + str(content) + '\n'
	with open(experiment + '_data.txt', 'a') as f:
		f.write(l)

def get_experiment_data(user, experiment, part):
	"""Gets part of data file for specific experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)
	if not(os.path.exists(experiment + '_data.txt')):
		return -1
	else:
		with open(experiment + '_data.txt' , 'r') as f:
			lines = [x.strip('\n') for x in f.readlines()]
			for l in lines:
				if l.startswith(str(part)):
					index = len(part) + 2
					return l[index:]
		return "Nada" #Nothing code

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
	a = a[1:-1]
	return a

def gen_gcard(user, experiment):
	"""Generates the gcard for new experiment"""
	os.chdir(basedir + '/users/' + user +'/projects/' + experiment)

	user_gcard = 'g.gcard'
	user_out = 'r.ev'
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
				ao_list = a.split(', ')
			if l.startswith('gl') :
				gl = l[4:]

	with open(basedir + '/components/expjson/' + ec + '.json') as data_file:
		stock_json = json.load(data_file)
		relevant_detectors = stock_json['detectors']

	if not(ao_list is None): #writing actual gcard, sees if ao used or not
		fo = open(user_gcard, "wb")
		fo.write("<gcard>" + '\n')
		for e in relevant_detectors:
			if e in ao_list:
				fo.write(e["tag"] + '\n')
			else:
				pass
		fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ gl +"'/>" + '\n')
		fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
		fo.write("</gcard>" + '\n')
		fo.close()
	else:
		fo = open(user_gcard, "wb")
		fo.write("<gcard>" + '\n')
		for e in relevant_detectors:
			fo.write(e["tag"] + '\n')
		fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ gl +"'/>" + '\n')
		fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
		fo.write("</gcard>" + '\n')
		fo.close()

def run_gemc(user,experiment):
	"""runs gemc"""
	os.chdir(basedir + '/users/' + user + '/projects/' + experiment) #change to correct dir
	user_gcard = 'g.gcard'

	with open('out.txt', 'w+') as out: #running process
		p = subprocess.Popen(args=['/bin/csh', '-c', "gemc " +  user_gcard + " -USE_GUI=0"], stdout=out)

		while 1:
			where = out.tell()
			line = out.readline()
			if not line:
				time.sleep(1)
				out.seek(where)
			else:
				if "Total gemc time:" in line:
					print line
					#kill gemc and close out.txt
					os.system('pkill -HUP gemc')
					p.kill()
					out.close()
					#return True for success
					return True
				elif "Abort" in line:
					print line
					#kill gemc and close out.txt
					os.system('pkill -HUP gemc')
					p.kill()
					out.close()
					#return False for failure:
					return False
				else:
					pass
