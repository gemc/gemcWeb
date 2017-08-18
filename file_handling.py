import os,time

PROJ_DIR = /group/clas/www/gemc2017/html/gemcWeb

def get_user_projects(user):
	"""Gets user projects and abstract to display on homepage"""
	projects = os.listdir(PROJ_DIR + '/users/' + user +'/projects')
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
	exp_dir = PROJ_DIR + '/components/expjson'
	for exp in os.listdir(exp_dir):
		if exp.endswith('.json'):
			possible_experiments.append(exp[:-5])
	return possible_experiments

def create_project_dir(user, experiment):
	"""Creates a directory for an experiment"""
	os.chdir(PROJ_DIR + '/users/' + user +'/projects/')
	os.mkdir(experiment)

def create_experiment_data(user, experiment):
	"""Creates the data file for specific experiment"""
	os.chdir(PROJ_DIR + '/users/' + user +'/projects/' + experiment)
	create = 'created: ' + time.strftime('%d/%m/%Y') + '\n'
	gcard = 'gcard: ' + PROJ_DIR + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.gcard\n'
	results = 'results: ' + PROJ_DIR + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.ev\n'
	with open(experiment + '_data.txt', 'w+') as f:
		f.write(str(create))
		f.write(str(gcard))
		f.write(str(results))

def rename_project_dir(user, experiment, title):
	os.chdir(PROJ_DIR + '/users/' + user + '/projects')
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
	oldgcard = 'gcard: ' + PROJ_DIR + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.gcard\n'
	oldresults = 'results: ' + PROJ_DIR + '/users/' + user + 'projects/' + experiment + '/' + experiment + '.ev\n'
	gcard = 'gcard: ' + PROJ_DIR + '/users/' + user + 'projects/' + title + '/' + title + '.gcard\n'
	results = 'results: ' + PROJ_DIR + '/users/' + user + 'projects/' + title + '/' + title + '.ev\n'

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

def write_experiment_data(user, experiment, part, content):
	"""Writes to data file for specific experiment"""
	os.chdir(PROJ_DIR + '/users/' + user +'/projects/' + experiment)
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
	os.chdir(PROJ_DIR + '/users/' + user +'/projects/' + experiment)
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
