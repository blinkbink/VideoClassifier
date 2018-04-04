import os
import uuid
import requests
from flask import Flask, jsonify, request, render_template, json
import cv2
import string
import random
import base64
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from decimal import Decimal

ALLOWED_EXTENSIONS = set(['mp4', 'jpg', 'png', 'jpeg'])

app = Flask(__name__)
app.secret_key = "Top Secret"

JsonData = []

s = URLSafeTimedSerializer("secret")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        compList = []
        id = uuid.uuid4().hex
        file = request.files['file']
        ktp = request.files['ktp']
        '''
        if form.data['file'] is None:
            return "Null Video"
        if form.data['ktp'] is None:
            return "Null KTP"
        '''

        #token = s.dumps(file.filename, salt="api")
        if (file and allowed_file(file.filename)) and (ktp and allowed_file(ktp.filename)):
            file.save(os.path.join("Video", id+".mp4"))
            ktp.save(os.path.join("ktp/face-"+id+".jpg"))
            if file.save:
                cam = cv2.VideoCapture("Video/"+id+".mp4")

                detector = cv2.CascadeClassifier('Classifiers/face.xml')

                img = cv2.imread("ktp/face-"+id+".jpg", cv2.IMREAD_COLOR)

                gray = cv2.imread("ktp/face-"+id+".jpg", cv2.IMREAD_GRAYSCALE)
                faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
                nig = 1

                for (x, y, w, h) in faces:
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), 2)

                    colorr = cv2.imread("ktp/face-"+id+".jpg", cv2.IMREAD_COLOR)
                    crop_img = colorr[y - 50:y + h + 50, x - 50:x + w + 50]
                    if nig > 1:
                        v = "dataKTP/face-"+id+".jpg"
                        cv2.imwrite(v, crop_img)
                    else:
                        v = "dataKTP/face-"+id+".jpg"
                        cv2.imwrite(v, crop_img)
                    nig = nig + 1
                    if not os.path.getsize(v):
                        os.remove(v)

                i = 0
                offset = 50
                #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
                #out = cv2.VideoWriter('Video/Vid-' + id_generator() + '.mp4', fourcc, 20.0, (640, 480))
                #ktp = base64.b64encode(open("dataKTP/face-" + id + ".png", "rb").read())

                ktp = base64.b64encode(open("dataKTP/face-"+id+".jpg", "rb").read())
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
                    for (x, y, w, h) in faces:
                        i = i + 1
                        print i
                        if i % 2 == 0:
                            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                            cv2.imwrite("dataVideo/face-"+id+'.'+str(i)+".png", im[y - 10:y + h + 10, x - 10:x + w + 10])
                            #cv2.rectangle(im, (x - 40, y - 40), (x + w + 40, y + h + 40), (225, 0, 0), 1)
                            #cv2.imshow('im', im[y - offset:y + h + offset, x - offset:x + w + offset])
                            cv2.waitKey(100)
                            image = "dataVideo/face-"+id+'.'+str(i)+".png"
                            image_64 = base64.b64encode(open(image, "rb").read())
                            compList.append(image_64)
                    #if i == countFrame:
                    if i == 20:
                        #file.close()
                        #out.release()
                        cam.release()
                        cv2.destroyAllWindows()

                        img = {'img1': ktp, 'img2': {'data': compList}}

                        jsondata = json.dumps(img)
                        jsondataasbytes = jsondata.encode('utf-8')

                        convert = 'img=' + jsondataasbytes

                        r = requests.post("http://localhost/test/index.py", data=convert)
                        break
                data = json.loads(r.text, parse_float=Decimal)

                hasil = data['hasilcompare'].split(",")

                new_list = []
                for item in hasil:
                    new_list.append(float(item))


                average = sum(new_list) / len(new_list)
                print (r.text+"{\"rata\" : \"" +str(average)+ "\"}")
                return r.text
            else:
                return "Unknow Error"
        else:
            return "Error File Extention not allowed"
    return render_template("main.html")

@app.route("/senddata", methods=['GET', 'POST'])
def senddata():
    try:
        respon = requests.post("http://localhost/test/index.py", data=json.dumps("string"))
        return "Success"+respon.content
    except Exception:
        return "Error"

@app.route("/api/<token>.json", methods=['GET', 'POST'])
def api(token):
    try:
        file = s.loads(token, salt="api", max_age=900) #time expired for 15 minutes
    except SignatureExpired:
        return "Token Expired"
    return jsonify({'data': JsonData})
    #post
    #response = requests.post("http://localhost:5000", json=JsonData)
    #return token
    # terima request json ke def
    # language = {'name' : request.json['name']
    # languages.append(language)
    # return jsonify({'languages' : languages})
#@app.route("/getdata", methods=['GET', 'POST'])
#def read():
    #post
    #response = requests.post("http://localhost:5000", json=JsonData)
    #return token
    # terima request json ke def
    # language = {'name' : request.json['name']
    # languages.append(language)
    # return jsonify({'languages' : languages})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
