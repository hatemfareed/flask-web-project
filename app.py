from collections import OrderedDict
import os
from random import randint
from flask import Flask, flash, redirect
import base64
from flask_mysqldb import MySQL



UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['PNG' , 'JPG' , 'JPEG' , 'GIF' , 'png', 'jpg', 'jpeg', 'gif','jfif'])

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

memcache = OrderedDict()

pages1 = {}
pages2 = {}
pages3 = {}
pages4 = {}
pages5 = {}
pages6 = {}

mysql = MySQL(app)

miss = []
hit = []
req = []
numOfItems = []
sizeCache = []



def allowed_file(filename):
	#print(filename.rsplit('.')[1])
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file2(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower()

def image_cache(file_path):
	ext =  allowed_file2(file_path)
	prefix = f'data:data:image/{ext};base64,'
	with open(file_path, 'rb') as f:
		img = f.read()
	x = prefix + base64.b64encode(img).decode('utf-8')
	return x 

def toDelete_orNot(id):
	curser = mysql.connection.cursor()
	curser.execute('SELECT path FROM todo WHERE id = %s' , [id])
	path = curser.fetchall()
	curser.execute('SELECT path FROM todo where path = %s' , [path])		
	share_path = curser.fetchall()
	if len(share_path) == 1:
		os.remove(path[0][0])
	mysql.connection.commit()
	curser.close()

def avg_hit():
	if len(hit) != 0:
		x = round((len(hit) / len(req)) * 100)
	else:
		x = 0
	return x
def avg_miss():
	if len(miss) != 0:
		x = round((len(miss) / len(req)) * 100)
	else:
		x = 0
	return x
def num_of_items():
	numOfItems.append(len(memcache))
	numOfItems.sort(reverse=True)
	return numOfItems[0]
def num_of_req():
	return len(req)

def total_size():	
	total = 0
	for i in memcache:
		total +=  (len(memcache[i]) * 3) / 4 - memcache[i].count('=', -2)
		sizeCache.append(total)
	size = "%.3f" %(total / (1024*1024))
	sizeCache.append(size)
	return float(size)

def get_size(key):
	size_key = (len(memcache[key]) * 3) / 4 - memcache[key].count('=', -2)
	toFloat = "%.3f" %(size_key / (1024*1024))
	return float(toFloat)

def dig_size():
	if len(memcache) != 0:
		x = max(memcache.values())	
		k =list(memcache.keys())[list(memcache.values()).index(x)]
		print(k)
		m = get_size(k)
	else:
		m = 0
	return  m

def policty_replacement(file_path , key):
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * FROM config order by id desc limit 1 offset 0")
	tasks = cursor.fetchone()
	mysql.connection.commit()
	cursor.close()
	if tasks is None:
		return redirect('/display')
	elif int(tasks[2]) == 1: #random
		req.append(key)
		table_size = tasks[1] 
		
		if key in memcache:
			hit.append(key)
		else:
			miss.append(key)
			memcache[key] = image_cache(file_path)
			if (total_size() > table_size) :
				
				if get_size(key) > table_size:
					memcache.pop(key)
					flash("The size of the image is greater than the size of the cache")
				else:
					print("********************************")
					memcache.pop(key)
					i = randint(0 , len(memcache) - 1)
					del memcache[list(memcache)[i]]
					memcache[key] = image_cache(file_path)
			if (total_size() > table_size):
				i = randint(0 , len(memcache) - 1)
				del memcache[list(memcache)[i]]
		print("*********",total_size(), '*********')
		
	else: #LRU
		
		req.append(key)
		table_size = tasks[1] 
		if key in memcache:
			hit.append(key)
			memcache.pop(key)
			memcache[key] = image_cache(file_path)
			
		else:
			miss.append(key)
			memcache[key] = image_cache(file_path)
			if(total_size() >= table_size) :
				if get_size(key) > table_size:
					memcache.pop(key)
					flash("The size of the image is greater than the size of the cache")
				else:
					print("hatem3")
					memcache.popitem(last=False)
					memcache[key] = image_cache(file_path)
			if (total_size() > table_size):
				memcache.popitem(last=False)
				
	print("*********",total_size(), '*********')

def key_found(key):
	req.append(key)
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * FROM config order by id desc limit 1 offset 0")
	tasks = cursor.fetchone()
	mysql.connection.commit()
	cursor.close()
	if tasks is None:
		return redirect('/display')
	elif int(tasks[2]) == 1: #random
		if key in memcache:
			hit.append(key)
	else: #LRU
		hit.append(key)
		memcache.move_to_end(key)
