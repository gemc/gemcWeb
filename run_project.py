import os, json, subprocess, time,

PROJ_DIR = /group/clas/www/gemc2017/html/gemcWeb

def trim_ec(e):
	"""Gets the user's experiment choice in usable form"""
	delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
	e = str(e)
	e = e.translate(None, delchars)
	return e

def get_ec_info(e, part):
	"""Gets the experiment desctiption for user ec"""
	with open(PROJ_DIR + '/components/expjson/' + e + '.json') as data_file:
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
	os.chdir(PROJ_DIR + '/users/' + user +'/projects/' + experiment)

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

	with open(PROJ_DIR + '/components/expjson/' + ec + '.json') as data_file:
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
	os.chdir(PROJ_DIR + '/users/' + user + '/projects/' + experiment) #change to correct dir
	user_gcard = experiment + '.gcard'

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
