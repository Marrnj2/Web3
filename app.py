from mongoengine import *
from flask import Flask, render_template
import csv
import os
app = Flask(__name__)
app.config.from_object('config')
# app.run(host='0.0.0.0', port=80)
db =connect('test')
db.drop_database('test')
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
                    countryCount = Country.objects(name=data[key])
                    if countryCount.count() == 0: 
                        country.name = data[key]
                    else:
                        country = countryCount[0]
                        dict = country.data
                else:
                    f = filename.replace(".csv","")
                    if f in dict:
                        dict[f][key] = data[key]
                    else:
                        dict[f] = {key:data[key]}
                    country.data = dict    
            country.save()
    countries = Country.objects
    return countries.to_json()


@app.route('/showData')
def showData(country=None):
    country = Country.objects.get
    return country.to_json()
        



@app.route('/show')
def showList():
        return render_template("showCountries.html")

@app.route('/Countries',methods=['GET'])
@app.route('/Countries/',methods=['GET'])
@app.route('/Countries/<name>', methods=['GET'])
def getCountries(name=None):
    if not Country.objects():
        return 'Server Error', 500
    else:
        country = None
        if name is None:
            country = Country.objects
            return country.to_json(),200

        else:
            country = Country.objects(name=name)
            if(country.count() == 0):
                return country.to_json(),400
        return country.to_json(),200


# Delete method 
@app.route('/Countries/<name>', methods=['DELETE'])
def deleteCountry(name):
    if not Country.objects():
        return 'Server Error', 500
    if name is None:
       return 'No Input Found',404
    else:
        if not Country.objects(name=name):
            return 'Not Found',400
        else:
            Country.objects(name=name).delete()
            return 'Success',204

# Add country 
@app.route('/Countries/<name>',methods=['POST'])
def saveCountry(name):
    if name is None:
        return 'No input',400
    elif not (isinstance(name,int)):
        return 'Numbers not allowed',404
    else:
        if Country.objects(name=name):
            return 'Country Already exists',400
        else:
            country = Country(name=name)
            country.save()
            return 'Success',201

if __name__ =="__main__":
    app.run(debug=True, port=8080)


#if __name__ =="__main__":
#    app.run(host='0.0.0.0', port=80)
