from fpdf import FPDF
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange
import sqlite3

from form import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FULL FLEMME'
Bootstrap(app)
database_conn = None  # DB Connector
database_filename = 'CRM.sqlite'



@app.route('/CRM_Boite_a_code/add_prospect', methods=['GET', 'POST'])
def addprospect():
    form = AddProspect()
    print('sdfghj')
    if form.validate_on_submit():
        print('poiuytre')
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "INSERT INTO LegalEntity (Name, N_siret, Address, Postalcode, City, Description, Url) VALUES " \
                f"({form.Name.data}, {form.N_siret.data},{form.Address.data}, {form.Postalcode.data}," \
                f" {form.City.data},{form.Description.data}, {form.Url.data})"
        print("aaaaaaa")
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.execute(query)
        return redirect(location="/CRM_Boite_a_code/add_comment")

    return render_template('titanic.html', form=form)


@app.route('/CRM_Boite_a_code/add_contact', methods=['GET', 'POST'])
def addcontact():
    form = AddContact()

    if form.validate_on_submit():
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "INSERT INTO Contact (LastName, FirstName, Email, Job, Phone, Status) VALUES " \
                f"('{form.LastName.data}', '{form.FirstName.data}','{form.Email.data}', '{form.Job.data}'," \
                f" '{form.Phone.data}','{form.Status.data}')"
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.execute(query)
        return redirect(location="/CRM_Boite_a_code/add_comment")
    return render_template('titanic.html', form=form)


@app.route('/CRM_Boite_a_code/modify_contact', methods=['GET', 'POST'])
def modifycontact():
    form = ModifyContact()

    if form.validate_on_submit():
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "UPDATE Contact (LastName, FirstName, Email, Job, City, Phone) SET " \
                f"({form.LastName.data}, {form.FirstName.data},'{form.Email.data}', '{form.Job.data}'," \
                f" {form.Phone.data},{form.Status.data}')"
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.execute(query)
        return redirect(location="/CRM_Boite_a_code/add_comment")
    return render_template('titanic.html', form=form)


@app.route('/CRM_Boite_a_code/add_comment', methods=['GET', 'POST'])
def addcomment():
    form = AddComment()

    if form.validate_on_submit():
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "INSERT INTO Comment (Description) VALUES " \
                f"('{form.Description.data}')"
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.execute(query)
        return redirect(location="/CRM_Boite_a_code")
    return render_template('titanic.html', form=form)

@app.route('/CRM_Boite_a_code')
def index():

    cur = database_conn.cursor()
    query = "SELECT Name, City FROM LegalEntity"
    result = cur.execute(query)
    return render_template('titanic_list.html', list=result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database_conn = sqlite3.connect(database_filename, check_same_thread=False)
    database_conn.execute('''CREATE TABLE IF NOT EXISTS LegalEntity
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            Name VARCHAR(50),
                            N_siret INT,
                            Address VARCHAR(255),
                            Postalcode INT,
                            City VARCHAR(50),
                            Description TEXT,
                            Url VARCHAR(250));''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS User
                            (Name VARCHAR(50),
                            Login VARCHAR(50),
                            Password VARCHAR(50));''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Contact
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            Lastname VARCHAR(50),
                            Firstname VARCHAR(50),
                            Email VARCHAR(100),
                            Job VARCHAR(50),
                            Phone VARCHAR(50),
                            Status VARCHAR(10));''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Comment
                            (Description TEXT,
                            Autor VARCHAR (50),
                            CreationDate DATE);''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Invoice
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            ContactID INT,
                            LegalEntityID INT);''')

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
