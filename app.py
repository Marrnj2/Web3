from flask import Flask, render_template
from mongoengine import *
app = Flask(__name__)
# app.run(host='0.0.0.0', port=80)
class User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()

connect('testDB')
@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    User(email="nick.marr@email.com",first_name="Nick",last_name="Marr").save()
    return render_template("index.html")


@app.route('/insperation')
def insperation():
    title = 'Insperation'
    return render_template('insperation.html',title=title)

@app.route("/listUsersTest")
def listUsersTest():
    return User.objects.to_json()


if __name__ =="__main__":
    app.run(host='0.0.0.0', port=80)
