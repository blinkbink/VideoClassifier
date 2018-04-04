#!/usr/bin/python2.7
import cgitb, cgi
import base64
import simplejson as json
import re
import face_recognition
import numpy as np
import io
from imageio import imread
from PIL import Image
import datetime
import os, errno
import shutil

cgitb.enable()
print("Content-Type: text/html;charset=utf-8")
print()
params = cgi.FieldStorage()
now = datetime.datetime.now()
date = str(now)
date2 = date.replace(" ","")
img = params.getvalue('img')
data1 = json.loads(img)
data2 = data1['img2']['data']


numparray = data1['img1']
numparray2 = numparray.replace(" ", "+")

b=bytes(numparray2, 'utf-8')
imgdata = base64.b64decode(b)

os.makedirs(date2)
with open(date2+"/img1.png", "wb") as f:
	f.write(imgdata)

image = face_recognition.load_image_file(date2+'/img1.png')

try:
	face_encode = face_recognition.face_encodings(image)[0]
	#print("face_encode = ".format(face_encode))
except IndexError:
	print("encode image failed")
	quit()

known_faces = []
y = 1
for images in data2:
	ir = images.replace(" ", "+")
	ib = bytes(ir, 'utf-8')
	imagedata = base64.b64decode(ib)
	x = str(y)
	with open(date2+"/compare"+x+".png", "wb") as g:
		g.write(imagedata)
	compare = face_recognition.load_image_file(date2+"/compare"+x+".png")
	try:
		compare_encode = face_recognition.face_encodings(compare)[0]
		#print("face_encode = ".format(face_encode))
	except IndexError:
		print("encode image compare failed")
		quit()
	known_faces.append(compare_encode)
	y = y+1

results = face_recognition.face_distance(known_faces, face_encode)

datahasil = []
#hasilakhir = "{"
for i, face_distance in enumerate(results):
	h = "{:.2}".format(face_distance, i)
	#hasilakhir = hasilakhir+"compare{}"
	datahasil.append(h)

hasilakhir = ','.join(datahasil)

shutil.rmtree(date2, ignore_errors=True)

print("{\"hasilcompare\" : \"" +hasilakhir+ "\"}")
