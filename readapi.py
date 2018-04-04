import requests
import json
import base64
from decimal import Decimal

file1 = base64.b64encode(open("dataVideo/face-099f850773f9482993664f6ee4b0c6b8.8.png", "rb").read())
file2 = base64.b64encode(open("dataVideo/face-099f850773f9482993664f6ee4b0c6b8.10.png", "rb").read())
file3 = base64.b64encode(open("dataVideo/face-099f850773f9482993664f6ee4b0c6b8.16.png", "rb").read())

img = {'img1': file1, 'img2': {'data': [file2, file3]}}

jsondata = json.dumps(img)
jsondataasbytes = jsondata.encode('utf-8')

convert = 'img='+jsondataasbytes

r = requests.post("http://localhost/test/index.py", data=convert)

#json = json.loads(r)
#hasil = json.get('hasilcompare')
#print hasil
#print r.text
#load the json to a string


data = json.loads(r.text, parse_float=Decimal)

hasil = data['hasilcompare'].split(",")

new_list = []
for item in hasil:
    new_list.append(float(item))

print sum(new_list) / len(new_list)
