from flask import Flask, render_template, session, redirect, url_for, flash, request
from . import main
from .forms import NamePhoneForm
from ..models import Interestedpeople, Foods
from app import db
import twilio.twiml


# Try adding your own number to this list!
callers = {
    "+14153099911": "Imanol",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
}

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NamePhoneForm()
    # capability = TwilioCapability(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    # capability.allow_client_outgoing(app.config['APP_SID'])
    # token = capability.generate()
    foods = Foods.query.all()
    if request.method == 'POST':
        name = request.values.get('name', None)
        phone = request.values.get('phone', None)
        interested = Interestedpeople(name=name, phone=phone)
        db.session.add(interested)
        db.session.commit()
        return redirect(url_for('main.index'))
    interestedpeople = Interestedpeople.query.all()
    return render_template('index.html', form=form, foods=foods, interestedpeople=interestedpeople)

@main.route('/foodsms', methods=['POST'])
def foodsms():
    foods = Foods.query.all()
    foodstring = ', '.join([str(x.name) for x in foods])
    if request.method == 'POST':
        keyword = request.values.get('Body', None)
        if keyword == 'FOOD':
            message = foodstring
        else:
            message = "This is West Sacramento Farm Stand, if you want to know which food is available text 'FOOD'."
        # reg = Friend(message=message,phone=phone)
        # db.session.add(reg)
        # db.session.commit()


    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
