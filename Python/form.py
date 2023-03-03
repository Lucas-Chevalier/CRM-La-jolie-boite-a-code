from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange
import sqlite3


class AddProspect(FlaskForm):
    Name = StringField('Nom*', validators=[DataRequired()])
    N_siret = IntegerField('Numero de siret*', validators=[DataRequired()])
    Address = StringField('Addresse*', validators=[DataRequired()])
    Postalcode = IntegerField('Code Postal*', validators=[DataRequired()])
    City = StringField('Ville*', validators=[DataRequired()])
    Description = StringField('Description')
    Url = StringField('URL du site')
    Submit = SubmitField('Submit')


class AddContact(FlaskForm):
    LastName = StringField('Nom*', validators=[DataRequired()])
    FirstName = StringField('Prenom*', validators=[DataRequired()])
    Email = StringField('Email*', validators=[DataRequired()])
    Job = StringField('Job')
    Phone = StringField('Téléphone')
    Status = SelectField('Statut*', choices=['Actif', 'Inactif'])
    Submit = SubmitField('Submit')


class ModifyContact(FlaskForm):
    LastName = StringField('Nom*', validators=[DataRequired()])
    FirstName = StringField('Prenom*', validators=[DataRequired()])
    Email = StringField('Email*', validators=[DataRequired()])
    Job = StringField('Job')
    Phone = StringField('Téléphone')
    Status = SelectField('Statut*', choices=['Actif', 'Inactif'])
    Submit = SubmitField('Submit')


class AddComment(FlaskForm):
    Description = StringField('Description*', validators=[DataRequired()])
    Submit = SubmitField('Submit')


class CreateInvoice(FlaskForm):
    pass



class User:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password






class LegalEntity:
    def __init__(self, name, n_siret, address, postalcode, city, description, url, nb_invoice, client):
        self.name = name
        self.n_siret = n_siret
        self.address = address
        self.postalcode = postalcode
        self.city = city
        self.description = description
        self.url = url
        self.nb_invoice = nb_invoice
        self.client = client


class Contact:
    def __init__(self, lastname, firstname, email, job, phone, status):
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.job = job
        self.phone = phone
        self.status = status


class Commentary:
    def __init__(self, description, autor, creationDate):
        self.description = description
        self.autor = autor
        self.creationDate = creationDate


class Invoice:
    def __init__(self, info, n_invoice, contact, legalEntity):
        self.info = info
        self.n_invoice = n_invoice
        self.contact = contact
        self.legalEntity = legalEntity
