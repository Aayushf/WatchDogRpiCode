from subprocess import Popen, PIPE
import RPi.GPIO as g
from time import time, sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from picamera import PiCamera
import random
cred = credentials.Certificate('/home/pi/pkrpi.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://evilwatchdog.firebaseio.com/',
    'storageBucket': 'evilwatchdog.appspot.com'
})

ref = db.reference('direction')
ref_logs = db.reference('logs').child('log_images')
ref_auto = db.reference('auto')
ref_feed = db.reference('live_feed')
bucket = storage.bucket()
def click_pic():
	stop()
	camera = PiCamera()
	t = int(time()*1000)
	camera.capture(str(t)+'.jpeg')
	print('Image Captured')
	blob = bucket.blob('logs/'+str(t)+'.jpeg')
	blob.upload_from_filename(str(t)+'.jpeg')
	print('Image Uploaded')
	ref_logs.update({str(t):'1'})
	camera.close()
US_T = 23
US_E = 18
M_1 = 21
M_2 = 16
M_3 = 12
M_4 = 7
PIR = 5
BZR = 9
T = 0.3
g.setmode(g.BCM)
g.setup(US_T, g.OUT)
g.setup(US_E, g.IN)
g.setup(M_1, g.OUT)
g.setup(M_2, g.OUT)
g.setup(M_3, g.OUT)
g.setup(M_4, g.OUT)
g.setup(PIR, g.IN)
g.setup(BZR, g.OUT)
def getDistance():
	#print('GetDistance Called')
	g.output(US_T, 1)
	sleep(0.01)
	g.output(US_T, 0)
	st = time()
	et = time()
	while g.input(US_E) == 0:
		st = time()
#		print('It is 0')
	while g.input(US_E) == 1:
		et = time()
#		print('It is 1')
	td = et-st
	d = 343000*td/20
    	#print('GetDistance ended')
	print('Nearest Obstacle Distance '+str(d))
	return d

def dirl():
	g.output(M_1, 1)
	g.output(M_2, 0)
	g.output(M_3, 0)
	g.output(M_4, 1)
def dirb():
	g.output(M_1, 1)
	g.output(M_2, 0)
	g.output(M_3, 1)
	g.output(M_4, 0)
def dirf():
	g.output(M_1, 0)
	g.output(M_2, 1)
	g.output(M_3, 0)
	g.output(M_4, 1)
def dirr():
	g.output(M_1, 0)
	g.output(M_2, 1)
	g.output(M_3, 1)
	g.output(M_4, 0)
def stop():
	g.output(M_1, 0)
	g.output(M_2, 0)
	g.output(M_3, 0)
	g.output(M_4, 0)
def move(direction):
	if direction == 'r':
		dirr()
	if direction == 'l':
		dirl()
	if direction == 'f':
		dirf()
	if direction == 'b':
		dirb()
	if direction == 's':
		stop()
lastnear = 0
rint = 0
last_live_feed = '0'
#sleep(30)
while True:
	lf = ref_feed.get()
	if lf == '1':
		if last_live_feed == '0':
			process = Popen(['/usr/bin/python3', '/home/pi/streamer.py'], stdout=PIPE, stderr=PIPE)
	if lf == '0':
		if last_live_feed == '1':
			process.kill()
	last_live_feed = lf
	rt = random.randint(2, 4)/10
	g.output(BZR, 1)
	if g.input(PIR) == 1:
		print('Intruder Detected')
		g.output(BZR, 0)
#		sleep(1)
		g.output(BZR, 1)
		click_pic()
		print("Capturing and Uploading Photo")
	a = ref_auto.get()
	a = '1'
	if a == '0':
		print('Manual Control')
		s = ref.get()
		move(s)
		print(s)
	else:
		d = int(getDistance())
#		if(d == lastdist):
#			dirb()
#			sleep(T)
#			continue
		print(d)
		if d<40:
			if lastnear == 0:
				rint = random.randint(0, 1)
			print(rint)
			if rint == 0:
				dirr()
			else:
				dirl()
			lastnear = 1
		elif lastnear == 1:
			lastnear = 0
		else:
			dirf()
		lastdist = d
g.cleanup()
