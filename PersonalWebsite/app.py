from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from wtforms.validators import Email, InputRequired
from wtforms.fields.html5 import EmailField
from flask_mail import Mail, Message
from pymongo import MongoClient
import random
import requests

app = Flask(__name__)
app.secret_key = 'today_is_a_wonderful_day'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'sangeethan.thaventhiran@gmail.com'
app.config["MAIL_PASSWORD"] = 'wobfchgzjsmnijsv'

mail = Mail(app)

#Email Form
class ContactForm(Form):
    name = StringField("Name",  [InputRequired()])
    email = EmailField("Email",  [InputRequired(), Email()])
    subject = StringField("Subject",  [InputRequired()])
    message = TextAreaField("Message",  [InputRequired()])
    submit = SubmitField("Send")

#Boolean to determine if the user is logged in
loggedIn = False

#Personal Database for About
client = MongoClient("mongodb+srv://SangeethanThaventhiran:Thaventhiran1@40125009-rtopv.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client.A3_SOEN287
educ = db.BIO_EDUCATION
exp = db.BIO_EXPERIENCE
project = db.BIO_PROJECTS
todolist = db.TODO

#External API's for Miscellaneous
POKEAPI = "https://pokeapi.co/api/v2/pokemon/"
ANIMEAPI = "https://api.jikan.moe/v3/anime/"
ANIME_LIST = [11061, 5114, 16498, 27631, 4186, 20785, 29803, 777, 14719, 38000, 37520, 20507, 9919, 1482, 6702, 23755, 22199, 28497]

#Landing Page
@app.route('/', methods = ['GET'])
def home():
    global loggedIn

    return render_template('home.html', loggedIn = loggedIn)

#About Page
@app.route('/bio', methods = ['GET'])
def bio():
    var1 = educ.find()
    var2 = exp.find()
    var3 = project.find()

    return render_template('biography.html', loggedIn = loggedIn, var1 = var1, var2 = var2, var3 = var3)

#Miscellaneous Page
@app.route('/misc')
def misc():

    #Pokemon API Sequence
    pokemonID = random.randint(1,808)
    pokeResponse = requests.get(POKEAPI+str(pokemonID))
    pokeName = pokeResponse.json()["forms"][0]["name"]
    pokeName = pokeName[0].upper() + pokeName[1:]
    pokeImg = pokeResponse.json()["sprites"]["front_default"]

    #Anime API Sequence
    animeID = ANIME_LIST[random.randint(0,len(ANIME_LIST))-1]
    animeResponse = requests.get(ANIMEAPI+str(animeID))
    animeName = animeResponse.json()["title_english"]
    animeImg = animeResponse.json()["image_url"]

    
    return render_template('miscellaneous.html', loggedIn = loggedIn, pokeName = pokeName, pokeImg = pokeImg, animeName = animeName, animeImg = animeImg)

#Information Page
@app.route('/info', methods= ['GET', 'POST'])
def info():
    form = ContactForm()
    if request.method == 'POST':
        msg = Message("WEBSITE: " + request.form['subject'], sender='sangeethan.thaventhiran@gmail.com', recipients=['sangeethan.thaventhiran@gmail.com'])
        msg.body = "From: " + request.form['name'] + " (" + request.form['email'] + ")\n" + request.form['message']
        mail.send(msg)
 
    elif request.method == 'GET':
        return render_template('information.html', loggedIn = loggedIn, form = form)

    return render_template('home.html', loggedIn = loggedIn, form = form)

#Login Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    global loggedIn
    loggedIn = False
    if request.method == 'POST':
        if request.form['username'] != 'sango' or request.form['password'] != 'pass':
            error = 'Invalid Credentials. Please try again.'
        else:
            loggedIn = True
            return redirect(url_for('home'))
            
    return render_template('login.html', error = error, loggedIn = loggedIn)

@app.route('/todo', methods = ['GET', 'POST'])
def todo():
    var4 = todolist.find()
    return render_template('todo.html', loggedIn = loggedIn, var4 = var4)

if __name__ == '__main__':
    app.run()