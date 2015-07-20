from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user
from . import main
from .forms import NamePhoneForm, EditProfileForm, EditProfileAdminForm, ProductForm
from ..models import Interestedpeople, Role, Foods, User, Permission, Product
from app import db
from ..decorators import admin_required, permission_required
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

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/manage-product', methods=['GET', 'POST'])
@login_required
def manage_product():
    form = ProductForm()
    if current_user.can(Permission.ADD_PRODUCT) and \
            form.validate_on_submit():
        product = Product(name=form.name.data, available=form.available.data,
                    farmer=current_user._get_current_object())
        db.session.add(product)
        return redirect(url_for('.manage_product'))
    form.name.data = ''
    products = Product.query.order_by(Product.name).all()
    return render_template('manage_product.html', form=form, products=products)
