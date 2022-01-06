from enum import unique
from . import db
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    registered_on = db.Column(db.DateTime, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    cart = db.relationship('Product', secondary='user_products')

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    marca = db.Column(db.String(150))
    modelo = db.Column(db.String(150))
    variante = db.Column(db.String(150))
    motor = db.Column(db.String(100))
    originalpw = db.Column(db.String(100))
    modifiedpw = db.Column(db.String(100))
    gainpw = db.Column(db.String(100))
    maxgainpw = db.Column(db.String(100))
    maxgainrpm = db.Column(db.String(100))
    originaltorque = db.Column(db.String(100))
    modtorque = db.Column(db.String(100))
    obd = db.Column(db.String(100))
    stg1 = db.Column(db.String(100))
    acc = db.Column(db.String(100))
    ron = db.Column(db.String(100))
    vmx = db.Column(db.String(100))
    cat = db.Column(db.String(100))
    egr = db.Column(db.String(100))
    dpf = db.Column(db.String(100))
    imm = db.Column(db.String(100))
    swr = db.Column(db.String(100))
    ms = db.Column(db.String(100))
    cat = db.Column(db.String(50))
    # prices
    pricestg1 = db.Column(db.String(100))
    pricestg2 = db.Column(db.String(100))
    dtcdecategronly = db.Column(db.String(100))
    pricecombo = db.Column(db.String(100))
    dpfonly = db.Column(db.String(100))
    dpfcombo = db.Column(db.String(100))
    # dealer prices
    dealerpricestg1 = db.Column(db.String(100))
    dealerpricestg2 = db.Column(db.String(100))
    dealerdtcdecategronly = db.Column(db.String(100))
    dealerpricecombo = db.Column(db.String(100))
    dealerdpfonly = db.Column(db.String(100))
    dealerdfpcombo = db.Column(db.String(100))
    # protocolos
    kess = db.Column(db.String(100))
    ktag = db.Column(db.String(100))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    product_price = db.Column(db.Float)
    product_dimensions = db.Column(db.String(150))
    product_description = db.Column(db.String(300))
    product_category = db.Column(db.String(100))
    image_path = db.Column(db.String(400))


class UserProducts(db.Model):
    __tablename__ = 'user_products'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer(), db.ForeignKey(
        'product.id', ondelete='CASCADE'))
