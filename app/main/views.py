from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user
from . import main
from .forms import NamePhoneForm, EditProfileForm, EditProfileAdminForm, ProductForm
from ..models import Interestedpeople, Role, User, Permission, Product
from app import db
from ..decorators import admin_required, permission_required
import twilio.twiml


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NamePhoneForm()
    farmers = User.query.filter_by(role_id = 1).all()
    # capability = TwilioCapability(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    # capability.allow_client_outgoing(app.config['APP_SID'])
    # token = capability.generate()
    products = Product.query.join(User).filter(User.role_id==1).all()
    if request.method == 'POST':
        name = request.values.get('name', None)
        phone = request.values.get('phone', None)
        interested = Interestedpeople(name=name, phone=phone)
        db.session.add(interested)
        db.session.commit()
        return redirect(url_for('main.index'))
    interestedpeople = Interestedpeople.query.all()
    return render_template('index.html', form=form, products=products, interestedpeople=interestedpeople, farmers=farmers)

@main.route('/foodsms', methods=['POST'])
def foodsms():
    products = Product.query.all()
    foodstring = ', '.join([x.name for x in products])
    if request.method == 'POST':
        keyword = request.values.get('Body', None).lower()
        if keyword == 'food':
            message = foodstring
        else:
            message = "This is West Sacramento Farm Stand, if you want to know which food is status text 'FOOD'."

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

@main.route('/user/<int:id>')
def user(id):
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/profile/<int:id>')
def profile(id):
    farmer = User.query.filter_by(id = id).first()
    return render_template('profile.html', farmer=farmer)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.farm_name = form.farm_name.data
        current_user.url = form.url.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', id=current_user.id))
    form.farm_name.data = current_user.farm_name
    form.url.data =current_user.url
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.url = form.url.data
        user.farm_name = form.farm_name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.list_users', id=current_user.id))
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.url.data = user.url
    form.farm_name.data = user.farm_name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/crop-list/<int:id>', methods=['GET', 'POST'])
@login_required
def crop_list(id):
    products = Product.query.filter_by(farmer_id = id).all()
    return render_template('crop_list.html', products=products)


@main.route('/crop-list/delete/<int:id>')
@login_required
def delete_product(id):
    print "clickaste para borrar"
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('.crop_list', id=product.farmer_id))


@main.route('/add-product/<int:id>', methods=['GET', 'POST'])
@login_required
def add_product(id):
    form = ProductForm()
    if current_user.can(Permission.ADD_PRODUCT) and \
            form.validate_on_submit():
        product = Product(name=form.name.data,
                    status=form.status.data,
                    price=form.price.data,
                    starts=form.starts.data,
                    ends=form.ends.data,
                    farmer=current_user._get_current_object())
        db.session.add(product)
        db.session.commit()
        form.name.data = ''
        form.price.data = ''
        form.starts.data = ''
        form.ends.data = ''
        return redirect(url_for('.crop_list', id=current_user.id))
    return render_template('add_product.html', form=form)

@main.route('/crop-list/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    print "clickaste para editar"
    product = Product.query.get_or_404(id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.status = form.status.data
        product.price = form.price.data
        product.starts = form.starts.data
        product.ends = form.ends.data
        db.session.add(product)
        db.session.commit()
        flash('The product has been updated.')
        return redirect(url_for('.crop_list', id=current_user.id))
    form.name.data = product.name
    form.status.data = product.status
    form.price.data = product.price
    form.starts.data = product.starts
    form.ends.data = product.ends
    return render_template('edit_product.html', form=form, product=product)

@main.route('/list-users')
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)
