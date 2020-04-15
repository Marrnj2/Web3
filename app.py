from mongoengine import *
from flask import Flask, render_template
import csv
import os
app = Flask(__name__)
app.config.from_object('config')
# app.run(host='0.0.0.0', port=80)
db =connect('CountryDB')
class Country(Document):
    name = StringField()
    data = DictField()
@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/insperation')
def insperation():
    title = 'Insperation'
    return render_template('insperation.html',title=title)

@app.route('/loadData')
def loadData():
       for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        f = open(path)
        r = csv.DictReader(f)
        d = list(r)
        for data in d:
            country = Country()
            dict = {}
            for key in data:
                if key == "country":
                    if(Country.objects(name__exists=key)):
                        country = Country.objects.get(name=key)
                        dict = country.objects.get(data)
                    else:
                        country = Country(name=key)

                else:
                    f = filename.replace(".csv","")
                    if f in dict:
                        dict[f][key] = data[key]
                    else:
                        dict[f] = {key:data[key]}
                    country = Country(data=dict[f])
                country.save()


            return "Done"

            
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


@app.route('/Countries/<name>', methods=['DELETE'])
def deleteCountry(name):
    Country.objects(name=name).delete()
    return render_template("showCountries.html")
    
@app.route('/Countries/<name>',methods=['POST'])
def saveCountry(name):
    country = Country(name=name)
    country.save()
    return country.to_json()


if __name__ =="__main__":
    app.run(debug=True, port=8080)


#if __name__ =="__main__":
#    app.run(host='0.0.0.0', port=80)
