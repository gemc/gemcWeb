import os, hashlib

PROJ_DIR = "/group/clas/www/gemc2017/html/gemcWeb"

def get_salty():
	"""Gets the salt"""
	os.chdir(PROJ_DIR)
	with open('salt.txt', 'r') as f:
		s = f.readline().strip()
	return s

salt = get_salty()

"""
To generate a salt run CL Python and run the following:

>>> import random
>>> ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(32))

Copy and paste this as your salt. Store it in a one line text file in the PROJ_DIR called salt.txt
"""

def create_account(user, password):
	"""Checks for new account validity. If valid, creates account"""
	if os.path.isdir(PROJ_DIR + '/users/' + user):
		return False
	else:
		#hashing and salting the password
		global salt
		password = password + salt
		hash_object = hashlib.sha256(password)
		hex_dig = hash_object.hexdigest()
		#creating user directory and storing pasword
		os.mkdir(PROJ_DIR + '/users/' + user)
		os.chdir(PROJ_DIR+ '/users/' + user)
		os.mkdir('projects')
		with open ('pwd.txt' , 'w') as f:
			f.write(hex_dig + '\n')
			return True

def account_exists(user):
	"""Checks if user account exists"""
	if os.path.isdir(PROJ_DIR + '/users/' + user):
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
	os.chdir(PROJ_DIR + '/users/' + user)
	with open('pwd.txt', 'r') as f:
		password = f.readline().strip()
	return password
