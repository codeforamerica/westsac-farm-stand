from flask import Flask, render_template, session, redirect, url_for, flash, request
from . import main
from .forms import NamePhoneForm
from ..models import Interestedpeople
from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NamePhoneForm()
    if request.method == 'POST':
        name = request.values.get('name', None)
        phone = request.values.get('phone', None)
        interested = Interestedpeople(name=name, phone=phone)
        db.session.add(interested)
        db.session.commit()
        return redirect(url_for('main.index'))
    interestedpeople = Interestedpeople.query.all()
    return render_template('index.html', form=form, interestedpeople=interestedpeople)
