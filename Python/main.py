import random
import time
from fpdf import FPDF
from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange
import sqlite3
from form import *
import os
from datetime import datetime
from weasyprint import HTML
import io
import uuid
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FULL FLEMME'
Bootstrap(app)
database_conn = None  # DB Connector
database_filename = 'CRM.sqlite'


@app.route('/CRM_Boite_a_code/login', methods=['GET', 'POST'])
def login():
    error = None
    database_conn = sqlite3.connect(database_filename, check_same_thread=False)
    cur = database_conn.cursor()
    query = "SELECT Login, Password FROM User"
    list = cur.execute(query).fetchall()
    result = []
    if request.method == 'POST':
        for result in list:
            if request.form['username'] != result[0] or request.form['password'] != result[1]:
                error = 'Invalid Credentials. Please try again.'
            else:
                cur.close()
                return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/CRM_Boite_a_code/add_login', methods=['GET', 'POST'])
def addlogin():
    error = None
    if request.method == 'POST':
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        cur = database_conn.cursor()
        query = "INSERT INTO User (Name, Login, Password) VALUES " \
        f"('{request.form['username']}','{request.form['login']}','{request.form['password']}');"
        print(query)
        cur.execute(query)
        database_conn.commit()
        #time.sleep(1)
        cur.close()
        database_conn.close()
        return redirect(url_for('index'))
    return render_template('add_login.html', error=error)


@app.route('/CRM_Boite_a_code/add_prospect', methods=['GET', 'POST'])
def addprospect():
    form = AddProspect()
    #print('sdfghj')
    if form.validate_on_submit():
        #print('poiuytre')
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "INSERT INTO LegalEntity (Name, N_siret, Address, Postalcode, City, Description, Url) VALUES " \
                f"('{form.Name.data}', {form.N_siret.data},'{form.Address.data}', {form.Postalcode.data}," \
                f" '{form.City.data}','{form.Description.data}', '{form.Url.data}')"
        #print("aaaaaaa")
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.commit()
        cur.close()
        database_conn.close()
        return redirect(location="/CRM_Boite_a_code/add_comment")

    return render_template('crm.html', form=form)


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
        database_conn.commit()
        cur.close()
        database_conn.close()
        return redirect(location="/CRM_Boite_a_code/add_comment")
    return render_template('crm.html', form=form)


@app.route('/CRM_Boite_a_code/modify_contact', methods=['GET', 'POST'])
def modifycontact():
    form = ModifyContact()

    if form.validate_on_submit():
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "UPDATE Contact (LastName, FirstName, Email, Job, City, Phone) SET " \
                f"('{form.LastName.data}', '{form.FirstName.data}','{form.Email.data}', '{form.Job.data}'," \
                f" '{form.Phone.data}','{form.Status.data}')"
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.commit()
        cur.close()
        database_conn.close()
        return redirect(location="/CRM_Boite_a_code/add_comment")
    return render_template('crm.html', form=form)


@app.route('/CRM_Boite_a_code/add_comment', methods=['GET', 'POST'])
def addcomment():
    form = AddComment()

    if form.validate_on_submit():
        database_conn = sqlite3.connect(database_filename, check_same_thread=False)
        query = "INSERT INTO Comment (Description) VALUES " \
                f"('{form.Description.data}')"
        cur = database_conn.cursor()
        cur.execute(query)
        database_conn.commit()
        cur.close()
        database_conn.close()
        return redirect(location="/CRM_Boite_a_code/add_prospect")
    return render_template('add_comment.html', form=form)

@app.route('/CRM_Boite_a_code/list_prospect', methods=['GET'])
def index():

       database_conn = sqlite3.connect(database_filename, check_same_thread=False)
       cur = database_conn.cursor()
       cur.execute("""SELECT Name, City FROM LegalEntity ORDER BY Name""")
       data_from_database = cur.fetchall()
       database_conn.commit()
       cur.close()
       database_conn.close()
       print(data_from_database)
       return render_template('prospect_list.html', data_from_database = data_from_database)

@app.route('/CRM_Boite_a_code/view_prospect', methods=['GET'])
def view_prospect():
    database_conn = sqlite3.connect(database_filename, check_same_thread=False)
    cur = database_conn.cursor()
    cur.execute("""SELECT Firstname, Lastname, Status FROM Contact WHERE Status = 'Actif' """)
    data_from_database = cur.fetchall()
    database_conn.commit()
    cur.close()
    database_conn.close()
    print(data_from_database)
    return render_template('view_prospect.html', data_from_database = data_from_database)

@app.route('/CRM_Boite_a_code/view_inactif_contact', methods=['GET'])
def view_inactif_contact():
    database_conn = sqlite3.connect(database_filename, check_same_thread=False)
    cur = database_conn.cursor()
    cur.execute("""SELECT Firstname, Lastname FROM Contact WHERE Status = 'Inactif' """)
    data_from_database = cur.fetchall()
    database_conn.commit()
    cur.close()
    database_conn.close()
    print(data_from_database)
    return render_template('inactif_contact.html', data_from_database = data_from_database)

@app.route('/CRM_Boite_a_code')
def connexion():
    return render_template('connexion.html')

@app.route('/CRM_Boite_a_code/invoice')
def invoive():
    today = datetime.today().strftime("%d/%m/%Y")
    invoice_number = 123
    from_addr = {
        'company_name': 'Python Tip',
        'addr1': '12345 Sunny Road',
        'addr2': 'Sunnyville, CA 12345'
    }
    to_addr = {
        'company_name': 'Nom du prospet',
        'person_name': 'Nom du contact',
        'campany_address': 'Adresse du prospect',
        'campany_sup_address': 'Code et Ville du prospect'
    }
    items = [
        {
            'title': 'website design',
            'charge': 300.00
        }, {
            'title': 'Hosting (3 months)',
            'charge': 75.00
        }, {
            'title': 'Domain name (1 year)',
            'charge': 10.00
        }
    ]
    duedate = datetime.today().strftime("%d/%m/%Y")
    total = sum([i['charge'] for i in items])
    rendered = render_template('invoice.html',
                               date=today,
                               from_addr=from_addr,
                               to_addr=to_addr,
                               items=items,
                               total=total,
                               invoice_number=invoice_number,
                               duedate=duedate)
    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf('./PDF/invoice.pdf')
    return send_file(
        './PDF/invoice.pdf'
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database_conn = sqlite3.connect(database_filename, check_same_thread=False)
    database_conn.execute('''CREATE TABLE IF NOT EXISTS LegalEntity
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            Name VARCHAR(50) NOT NULL,
                            N_siret INT NOT NULL,
                            Address VARCHAR(255) NOT NULL,
                            Postalcode INT NOT NULL,
                            City VARCHAR(50) NOT NULL,
                            Description TEXT,
                            Url VARCHAR(250));''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS User
                            (Name VARCHAR(50),
                            Login VARCHAR(50),
                            Password VARCHAR(50));''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Contact
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            Lastname VARCHAR(50)NOT NULL,
                            Firstname VARCHAR(50)NOT NULL,
                            Email VARCHAR(100)NOT NULL,
                            Job VARCHAR(50),
                            Phone VARCHAR(50),
                            Status VARCHAR(10)NOT NULL);''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Comment
                            (Description TEXT NOT NULL,
                            Autor VARCHAR (50),
                            CreationDate DATE NOT NULL DEFAULT CURRENT_TIMESTAMP);''')
    database_conn.execute('''CREATE TABLE IF NOT EXISTS Invoice
                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT    NOT NULL,
                            ContactID INT,
                            LegalEntityID INT);''')

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/