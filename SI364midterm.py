###############################
####### SETUP (OVERALL) #######
###############################

import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, InputRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import simplejson as json

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'yikes'
## Statements for db setup (and manager setup if using Manager)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/midterm364"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################
class Brewery(db.Model):
    __tablename__ = "brewery"
    id = db.Column(db.Integer,primary_key=True)
    brewery = db.Column(db.String(140))
    name_id = db.Column(db.Integer, db.ForeignKey('name.id'))


class Name(db.Model):
    __tablename__ = "name"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    brewery = db.relationship('Brewery', backref=db.backref('Name', lazy = True))





###################
###### FORMS ######
###################

class BrewForm(FlaskForm):
    name = StringField("Please enter your name",validators=[InputRequired()])
    brewery = StringField('Please enter a brewery', validators = [InputRequired()])
    def validate_brewery(self, field):
        if field.data[0].islower():
            raise ValidationError('First letter must be capitalized')
    submit = SubmitField("Submit")



#######################
###### VIEW FXNS ######
#######################

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/addNew', methods = ['GET','POST'])
def add():
    form = BrewForm()
    name = form.name.data
    brew = form.brewery.data
    return render_template('addNew.html',form=form)

@app.route('/getBrew', methods = ['GET','POST'])
def brew():
    form = BrewForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        brewery_name = form.brewery.data
        breweries = Brewery.query.all()
        dup = 0
        namebool = 0
        brewbool = 0
        name_id = ""
        for x in breweries:
            user = Name.query.filter_by(id=x.name_id).first()
            if user.name == name:
                namebool = 1
                name_id = x.name_id
            if x.brewery == brewery_name:
                brewbool = 1
            if user.name == name and x.brewery == brewery_name:
                dup = 1
        print(brewbool, namebool, dup)
        if dup != 1:
            if namebool == 0:
                user = Name(name=name)
                db.session.add(user)
                db.session.commit()
                brewery = Brewery(brewery= brewery_name, name_id = user.id)
                db.session.add(brewery)
                db.session.commit()
            else:
                brewery = Brewery(brewery= brewery_name, name_id = name_id)
                db.session.add(brewery)
                db.session.commit()
        res = requests.get('https://api.openbrewerydb.org/breweries?by_name={}'.format(brewery_name))
        dic = json.loads(res.text)
        return render_template('brew.html', name = name, brewname = brewery_name, state = dic[0]['state'], type = dic[0]['brewery_type'], phone = dic[0]['phone'])

    flash(form.errors)
    return redirect(url_for('add'))

@app.route('/showAll')
def showAll():
    breweries = Brewery.query.all()
    final = []
    for x in breweries:

        user = Name.query.filter_by(id=x.name_id).first()
        tup = (user.name, x.brewery)
        final.append(tup)
    return render_template('name.html',full_list = final)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
