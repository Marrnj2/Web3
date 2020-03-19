from flask import Flask, render_template
from mongoengine import *
app = Flask(__name__)
app.config.from_object('config')
# app.run(host='0.0.0.0', port=80)
connect('testDB')
class User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    for file in os.listfir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        f = open(path)
        r = csv.reader(f)
        d = list(r)
        for data in d:
            print(data)
    #User(email="nick.marr@email.com",first_name="Nick",last_name="Marr").save()
    return render_template("index.html")


@app.route('/insperation')
def insperation():
    title = 'Insperation'
    return render_template('insperation.html',title=title)

@app.route("/listUsersTest")
def listUsersTest():
    return User.objects.to_json()

@app.route('/users', methods=['GET'])
@app.route('/users/<user_id>',methods=['GET'])
def getUsers(user_id=None):
    users = None
    if user_id is None:
        users = User.objects
    else:
        users = User.objects.get
    return users.to_json()
    
if __name__ =="__main__":
    app.run(debug=True, port=8080)

#if __name__ =="__main__":
#    app.run(host='0.0.0.0', port=80)
