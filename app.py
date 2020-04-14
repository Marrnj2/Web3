from mongoengine import *
from flask import Flask, render_template
import csv
import os
app = Flask(__name__)
app.config.from_object('config')
# app.run(host='0.0.0.0', port=80)
connect('CountrieDB')

class Country(Document):
    name = StringField(required=True)

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        f = open(path)
        r = csv.reader(f)
        d = list(r)
        for data in d:
            newCountry = Country(name=data[0])
    return render_template("index.html")


@app.route('/insperation')
def insperation():
    title = 'Insperation'
    return render_template('insperation.html',title=title)

@app.route('/loadData')
def loadData():
        NZ = Country(name="New Zealand")
        NZ.save()
        Korea = Country(name="Korea")
        Korea.save()
        all_countrys = [{'name'}]
        return 'country saved'

@app.route('/showData')
def showData(country=None):
    country = Country.objects.get
    return country.to_json()
        



@app.route('/show')
def showList():
        return render_template("showCountries.html")

@app.route('/Countries',methods=['GET'])
@app.route('/Countries/<name>', methods=['GET'])
def getCountries(name=None):

    country = None
    if name is None:
        country = Country.objects
    else:
        country = Country.objects.get(name=name)
    return country.to_json()


#@app.route('countrys/<name>', methods=['PUT'])
    
#@app.route('countrys/<name>',methods=['POST'])


if __name__ =="__main__":
    app.run(debug=True, port=8080)


#if __name__ =="__main__":
#    app.run(host='0.0.0.0', port=80)
