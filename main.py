from __future__ import barry_as_FLUFL
from asyncio import sleep
from cgitb import reset
from datetime import datetime
from http.client import CannotSendHeader
from operator import index
import os
from pydoc import pager
from random import randint
from re import I, L
from webbrowser import get
from flask import  render_template, request, redirect ,flash
from pyparsing import Iterable
from sqlalchemy import false
from werkzeug.utils import secure_filename
from flask import json
from flask_sqlalchemy import SQLAlchemy
from app import *
from flask_mysqldb import MySQL
import time
import base64
from io import BytesIO
from PIL import Image
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from collections import OrderedDict



start_time = time.time()
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
scheduler = BackgroundScheduler()
scheduler.start()



def interval_task():
	
	with app.app_context():
		cursor = mysql.connection.cursor()
		cursor.execute("INSERT INTO statistic (miss_rate ,hit_rate ,number_of_requests , number_of_item ,total_size , DATETIME) VALUES (%s,%s,%s,%s,%s,%s)" , (avg_miss() , avg_hit() , num_of_req() , num_of_items(), total_size() , datetime.now()))		
		mysql.connection.commit()
		cursor.close()
scheduler.add_job(func=interval_task, trigger="interval", seconds=5) 




def delay():
	with app.app_context():
		
		cursor = mysql.connection.cursor()
		# cursor.execute("DELETE FROM statistic")
		
		pages1.clear() ;pages2.clear();pages3.clear();pages4.clear();pages5.clear();pages6.clear()
		
		cursor.execute("SELECT * FROM statistic ORDER BY id DESC LIMIT 119")
		tasks = cursor.fetchall()
		
		if tasks is not None: #and len(tasks) >=10:
			for i in range(len(tasks)):
				pages1[i] = tasks[i][1]
				pages2[i] = tasks[i][2]
				pages3[i] = tasks[i][3]
				pages4[i] = tasks[i][5]
				pages5[i] = tasks[i][6]
				pages6[i] = tasks[i][4]

		mysql.connection.commit()
		cursor.close()

scheduler.add_job(func=delay, trigger="interval", minutes=10) # minutes

@app.route("/statistic")
def statistic():
	
	return render_template('statistic.html' , tasks1 = pages1 , tasks2 = pages2,
												tasks3 = pages3 , tasks4 = pages4 ,
												tasks5 = pages5 , tasks6 = pages6 ,
												length = len(pages1))
	


@app.route('/')
def upload_form():
	print(f"the size of cache is :{total_size()}MB")
	# print(f"the number of items in cache is :{num_of_items()}")
	return  render_template('upload.html' , title = "Upload Image") 

@app.route('/', methods=['POST'])
def upload_image():
	
	curser = mysql.connection.cursor()
	file = request.files['file']
	key = request.form['key']
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	if request.method == 'POST':
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)

			try:
				curser.execute("INSERT INTO todo (key_img , path) VALUES (%s , %s)" , (key , file_path))
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

				#memcache[key] = image_cache(file_path) # cached image
				policty_replacement(file_path, key)
				
				print('upload_image filename: ' + file.filename)
				flash('Image successfully uploaded and displayed below') 

				mysql.connection.commit()
				curser.close()
				return render_template('upload.html', filename=filename , title = "Upload Image") 
				
			except:
				curser.execute('SELECT id FROM todo WHERE key_img = %s' , (key,))
				data = curser.fetchone()
				delete(data[0])
				mysql.connection.commit()
				curser.close()
				upload_image()
				flash('the path is updated')
				return redirect(request.url)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif , PNG , JPG , JPEG , GIF')
			return redirect(request.url)

@app.route('/display')
def display():
	print(dig_size())
	return render_template("display.html")

@app.route('/display' ,methods=['POST' ,'GET'] )
def display_image():
	st = time.time()
	curser = mysql.connection.cursor()
	key = request.form['key']
		
	try:
		if key not in memcache:
			curser.execute("SELECT * FROM todo WHERE key_img = %s" , [key])
			task = curser.fetchone()

			curser.execute("SELECT * FROM config")
			config = curser.fetchone()
			if config is None:
				flash("please set the cache configuration")
				return render_template('displayIMG.html' , filename = task[2] , key= key)
			mysql.connection.commit()
			curser.close()
			
			if task is None:
				req.append(key)
				miss.append(key)
				response = app.response_class(
				response=json.dumps("Unknown key"),
				status=400,
				mimetype='application/json'
			)
				return response
			else:
				response = app.response_class(
				response=json.dumps(key),
				status=200,
				mimetype='application/json' 
				)
				
				policty_replacement(task[2] , key)
				print("its in database")
				et = time.time()
				print("the time is : " , et - st) # TIME IN DATABASE
				for i in memcache:
					print(i)
				return render_template('displayIMG.html' , filename = task[2] , key= key)
				
		else:
			print("its in memcache")
			key_found(key)
			# i = memcache[key]
			et = time.time()
			
			print("the time is : " , et - st) # TIME IN MEMCACHE
			for i in memcache:
				print(i)
			return render_template('displayIMG.html' , filename = memcache[key] , key = key)	
		
	except:
		return redirect('/display')

@app.route('/list' )
def list():
	curser = mysql.connection.cursor()
	curser.execute("SELECT * FROM todo ")
	tasks = curser.fetchall()
	mysql.connection.commit()
	curser.close()
	
	return render_template('list.html', tasks=tasks  ,  titel = "Image")
	


@app.route('/delete/<int:id>')
def delete(id):

	curser = mysql.connection.cursor()
	try:
		#for delete img in folder
		toDelete_orNot(id)
		curser.execute('SELECT key_img FROM todo WHERE id = %s' , [id])
		index = curser.fetchone()
		curser.execute("DELETE FROM todo WHERE id = %s" , [id])
		print(index[0],"****************")
		if index[0] in memcache:
			del memcache[index[0]]
		mysql.connection.commit()
		curser.close()
		flash( 'Image successfully deleted')
		return redirect('/list')
	except:
		flash('Image not found')
		return redirect('/list')


@app.route('/update/<int:id>' , methods=['POST', 'GET'])
def update(id):
	curser = mysql.connection.cursor()
	curser.execute('SELECT id,key_img FROM todo WHERE id = %s' , (id,))
	data = curser.fetchone()

	if request.method == 'POST':
		file = request.files['file']
		try:
			if file and allowed_file(file.filename):
				file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
				#for delete img in folder
				toDelete_orNot(id)
				curser.execute('UPDATE todo SET path = %s WHERE id = %s', (file_path , data[0]))
				# memcache[data[1]] = image_cache(file_path)
				policty_replacement(file_path , data[1])
				file.save(file_path)
				mysql.connection.commit()
				curser.close()
				return redirect('/list')
		except:
			flash('Allowed image types are -> png, jpg, jpeg, gif , PNG , JPG , JPEG , GIF')
			return redirect('/list')
	else:
		return render_template('update.html', task= data[0])

@app.route('/config' , methods=['POST', 'GET'])
def config():
	curser = mysql.connection.cursor()
	current =  total_size()
	curser.execute("SELECT * FROM config")
	tasks = curser.fetchall()
	if request.method == 'POST':
		try:
			policty =  request.form['policty']
			capacity = request.form['capacity']
			if current > float(capacity):
				flash(f'the capacity({capacity})MB is less than the current size({current})MB')
				size = abs(current - float(capacity))
				if int(policty) == 2:
					while(total_size() >= float(capacity)):
						for i in memcache:
							if size > get_size(i):
								size -= get_size(i)
								del memcache[i]
							else:
								del memcache[i]
						
				else:
					while(total_size() >= float(capacity)):
							r = randint(0 , len(memcache) - 1)
							print(r)
							if size > get_size(r):
								size -= get_size(r)
								del memcache[list(memcache)[r]]
							else:
								del memcache[list(memcache)[r]]
						
							
					
			curser.execute('select policty from replacement where id = %s',(policty))
			data = curser.fetchone()
			print("%s" %data[0])
			curser.execute('INSERT INTO config (capacity, policty) VALUES (%s , %s)' , [capacity,policty])	
			

			mysql.connection.commit()
			curser.close()
			
			return redirect('/config')
		except:
			flash('Error')
			return redirect('/config')
	else:
		return render_template('config.html', tasks=tasks ,chas = memcache,  titel = "Config")


@app.route('/clear')
def clear():
	try:
		curser = mysql.connection.cursor()
		curser.execute('DELETE FROM config')
		memcache.clear()
		mysql.connection.commit()
		curser.close()
		return redirect('/config')
	except:
		flash('Error')
		return redirect('/config')
	


if __name__ == "__main__":
	app.run(debug=False)

# CREATE TABLE replacement(
# 	id int ,
#     policty varchar(20) , 
#     primary key (id)
# );

# CREATE TABLE config(
# 	id int AUTO_INCREMENT ,
#     capacity int NOT NULL ,
#     policty int ,
#     primary key (id) ,
#     FOREIGN key (policty) REFERENCES replacement(id)
# );

