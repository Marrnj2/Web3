from mongoengine import *
from flask import Flask, render_template
from flask_cors import CORS
import csv
import os
app = Flask(__name__)
CORS(app)
app.config.from_object('config')
# app.run(host='0.0.0.0', port=80)
connect(app.config['CountryDB'],username=app.config["marrnj2"],password=app.config['SuperSecure'],authentication_source=app.config['CountryDB'])

class Country(Document):
    name = StringField()
    data = DictField()
     
@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")

# Directs users to insperation page
@app.route('/insperation')
def insperation():
    title = 'Insperation'
    return render_template('insperation.html',title=title)


@app.route('/documentation')
def documentation():
    return render_template('docs.html')

# Drops all tables in the database
@app.route('/dropData')
def dropData():
    db.drop_database('test')
    return 'Data Gone'

# Loads data from csv's
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
        

# List Countries 
# GET /Countries Lists all countries if it exists
# GET /Countries/<optional:name> lists the specified country if it exists
# Optional Parameters
# name (string) name used to specify the desired country
# Example
# Get /Countries
# Returns
#[
#   {
#       name: "Australia"
#       data:
#   },
#   {
#       name: "Canada"
#       data:
#   }
#
# ]
#  Get /Countries/Rwanda
#[
#   {
#       name: Rwanda
#       data:
#   }
# ]
# Errors
# Server side error - status code 500
# Country was not found - status code  404
# Successful deletion - status code 200


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
                return 'Country not found',404
        return country.to_json(),200


# Delete Country
# Removes a country from the database 
# DELETE /Countries/<name> Deletes the specified country if it exists

# Example 
# DELETE /Countries/Mongolia
# returns Success - 204
# Errors
# Server side error - 500
# Bad user request - 400
# Country was not found - 404
# Successful deletion - 204
# Example
# DELETE /Countries/
# returns No Input Found status code 400
@app.route('/Countries/<name>', methods=['DELETE'])
def deleteCountry(name):
    if not Country.objects():
        return 'Server Error', 500
    if name is None:
       return 'No Input Found',400
    else:
        if not Country.objects(name=name):
            return 'Not Found',404
        else:
            Country.objects(name=name).delete()
            return 'Success',204


# Add country 
# Adds a country to the database
# POST /Countries/<name> - Adds submited country if it does not yet exist

# Example 
# POST /Countries/Taiwan
# Returns 
# Success - status 201
# Errors 
# Server side error - 500
# Bad user request - 400
# Country was not found - 404
# Successful addition - 201
# Example
# POST /Countries/7
# returns Numbers are not countries - status code 400
@app.route('/Countries/<name>',methods=['POST'])
def saveCountry(name):
    if name is None:
        return 'No input',400
    else:
        if Country.objects(name=name):
            return 'Country already exists',400
        else:
            country = Country(name=name)
            country.save()
            return 'Success',201

# if __name__ =="__main__":
#    app.run(debug=True, port=8080)


if __name__ =="__main__":
    app.run(host='0.0.0.0', port=80)
