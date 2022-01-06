from flask import Blueprint, render_template, request, flash, redirect, Response
from flask.helpers import url_for
from flask_mail import Mail, Message
from website.auth import login
from .models import User, Product, Role, Auto
from website import create_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db, allowed_file
from flask_login import login_user, login_required, logout_user, current_user
from flask_user import roles_required, UserManager, UserMixin
import os
import random
from csv import reader

views = Blueprint('views', __name__)
app = create_app()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "quantumprinting3d@gmail.com",
    "MAIL_PASSWORD": "Peugeot307xtp"
}
app.config.update(mail_settings)
mail = Mail(app)

# fabricantes = ["Abarth", "Audi", "BMW", "Chevrolet", "Citroen", "Dodge RAM", "Ford", "Ford Camiones", "Fiat", "Honda", "Hyundai", "Iveco Camiones", "Jeep",
#                "Mercedes Benz", "Mercedes Benz Camiones", "Mini", "Nissan", "Peugeot", "Renault", "Scania Camiones", "Suzuki", "Toyota", "Volkswagen", "VW Camiones", "Volvo Camiones"]


@views.route('/', methods=["GET", "POST"])
def home():
    # POST requests
    if request.method == "POST":
        # client_name = request.form.get("name")
        # client_email = request.form.get("email")
        # subject = request.form.get("subject")
        # message = request.form.get("message")

        select = request.form.get('comp_select')
        modeloInput = request.form.get('comp_select_1')
        autoSelected = Auto.query.filter_by(
            modelo=modeloInput).first()
        autoId = autoSelected.id
        return redirect("/autos/" + str(autoId))

        # msg = Message('Nueva consulta de' + client_email,
        #               sender='quantumprinting3d@gmail.com', recipients=["quantumprinting3d@gmail.com"])
        # msg.body = message
        # mail.send(msg)
        # flash('Mensaje enviado', category='success')

    # select algorithm
    fabricantes = []
    objQuery = Auto.query.all()
    for auto in objQuery:
        marca = auto.marca
        if marca in fabricantes:
            pass
        else:
            fabricantes.append(marca)
    i = 0
    portfolioObj = []
    # portfolio algorithm
    for i in range(6):
        auto = random.choice(objQuery)
        portfolioObj.append(auto)

    print(portfolioObj)

    return render_template("index.html", user=current_user, autos=Auto.query.all(), fabricantes=fabricantes, portfolioObj=portfolioObj)


@views.route('/autos/<int:id>')
def autos(id):

    return str(id)


@views.route('/join')
def join():
    return render_template("join.html", user=current_user)


@views.route('/tienda')
def tienda():
    # products = Product.query.all()
    return render_template("gallery.html", user=current_user, products=Product.query.all())


@views.route('/pedidos')
@login_required
def pedidos():
    return render_template("pedidos.html", user=current_user)


@views.route('/add', methods=["GET", "POST"])
@login_required
@roles_required("Admin")
def add():
    products = Product.query.all()
    if request.method == "POST":
        productName = request.form.get("productName")
        productPrice = request.form.get("productPrice")
        productDimensions = request.form.get("productDimensions")
        productDescription = request.form.get("productDescription")
        productCategory = request.form.get("productCategory")
        pic = request.files['pic']

        if not pic:
            flash('Agregar foto', category='error')
        else:
            newProduct = Product(product_name=productName,
                                 product_price=productPrice, product_dimensions=productDimensions, product_description=productDescription, product_category=productCategory)
            db.session.add(newProduct)
            db.session.commit()

            if allowed_file(pic.filename):
                filename = secure_filename(pic.filename)
                splitFilename = os.path.splitext(filename)
                newFilename = str(newProduct.id) + splitFilename[1]
                print(newFilename)
                image_path = url_for(
                    'static', filename='products/' + newFilename)
                pic.save(app.config['UPLOAD_FOLDER'] + newFilename)
                newProduct.image_path = image_path
                flash('product added', category='success')
                print(newFilename)
                print(image_path)
                db.session.commit()
                # userProducts = [newProduct, ]
                # current_user.cart = userProducts

    return render_template('add.html', user=current_user)


@views.route('/changeprice', methods=["GET", "POST"])
def change_price():
    products = Product.query.all()
    if request.method == "POST":
        productName = request.form.get("productName")
        newProductPrice = request.form.get("productPrice")

        product_to_change = Product.query.filter_by(
            product_name=productName).first()

        product_to_change.product_price = newProductPrice

        db.session.commit()
        flash('Producto actualizado', category='success')

    return render_template('change.html', user=current_user)


@views.route("/admin", methods=["GET", "POST"])
@login_required
@roles_required("Admin")
def admin_dashboard():
    return render_template("dashboardtemp.html", roles=Role.query.all(), users=User.query.all(), current_user=current_user)


@views.route("/database", methods=["GET", "POST"])
def database():
    with open('E:/Coding/Flask/DataRacing/website/static/csv/newCsv.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        attributes = dir(Auto)
    return render_template("database_table.html", roles=Role.query.all(), users=User.query.all(), user=current_user, products=Product.query.all(), autos=Auto.query.all(), header=header, attributes=attributes)


@views.route('/cart')
@login_required
def cart():
    total_items = 0
    total_price = 0
    for p in current_user.cart:
        total_items += 1
        total_price += p.product_price
    return render_template("cart.html", roles=Role.query.all(), users=User.query.all(), user=current_user, products=Product.query.all(), current_user=current_user, total_items=total_items, total_price=total_price)


@views.route('/addcart/<int:id>')
@login_required
def addcart(id):
    cart_product = Product.query.filter_by(id=id).first()
    current_user.cart.append(cart_product)
    db.session.commit()
    flash('Producto añadido', category='success')
    return render_template("shop.html", roles=Role.query.all(), users=User.query.all(), user=current_user, products=Product.query.all(), current_user=current_user)


@views.route('/removecart/<int:id>')
@login_required
def removecart(id):
    cart_product = Product.query.filter_by(id=id).first()
    for product in current_user.cart:
        if product.id == id:
            current_user.cart.remove(product)
    db.session.commit()
    flash('Producto añadido', category='success')
    return render_template("cart.html", roles=Role.query.all(), users=User.query.all(), user=current_user, products=Product.query.all(), current_user=current_user)


@views.route('/product/<int:id>')
def product(id):
    product = Product.query.filter_by(id=id).first()
    return render_template("product-details.html", roles=Role.query.all(), users=User.query.all(), user=current_user, product=product, current_user=current_user)


@views.route('/updatecsv')
def updatecsv():
    text = open("E:/Coding/DataRacing/website/static/csv/newCsv.csv", "r")
    text = ''.join([i for i in text]) \
        .replace(" ", "False")
    x = open("E:/Coding/DataRacing/website/static/csv/newCsv.csv", "w")
    x.writelines(text)
    x.close()
    return render_template("home.html", roles=Role.query.all(), users=User.query.all(), user=current_user, current_user=current_user)


@views.route('/addcsv', methods=["GET", "POST"])
def addcsv():
    products = Product.query.all()
    if request.method == "POST":
        csv = request.files['csv']
        csv.save(os.path.join(
            "E:\Coding\Flask\DataRacing\website\static\csv", "newCsv.csv"))
        with open('E:/Coding/Flask/DataRacing/website/static/csv/newCsv.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)

            for row in csv_reader:
                itemLoop = 0
                idLoop = 0
                newCar = Auto()
                db.session.add(newCar)
                db.session.commit()
                carNew = Auto.query.filter_by(id=idLoop).first()
                autosQ = Auto.query.all()

                newCar.code = row[0]
                newCar.tipo = row[1]
                newCar.marca = row[2]
                newCar.modelo = row[3]
                newCar.variante = row[4]
                newCar.motor = row[5]
                newCar.originalpw = row[6]
                newCar.modifiedpw = row[7]
                newCar.gainpw = row[8]
                newCar.maxgainpw = row[9]
                newCar.maxgainrpm = row[10]
                newCar.originaltorque = row[11]
                newCar.modtorque = row[12]
                newCar.obd = row[13]
                newCar.stg1 = row[14]
                newCar.acc = row[15]
                newCar.ron = row[16]
                newCar.vmx = row[17]
                newCar.cat = row[18]
                newCar.egr = row[19]
                newCar.dpf = row[20]
                newCar.imm = row[21]
                newCar.swr = row[22]
                newCar.ms = row[23]
                newCar.cat = row[24]
                newCar.pricestg1 = row[25]
                newCar.pricestg2 = row[26]
                newCar.dtcdecategronly = row[27]
                newCar.pricecombo = row[28]
                newCar.dpfonly = row[29]
                newCar.dpfcombo = row[30]
                newCar.dealerpricestg1 = row[31]
                newCar.dealerpricestg2 = row[32]
                newCar.dealerdtcdecategronly = row[33]
                newCar.dealerpricecombo = row[34]
                newCar.dealerdpfonly = row[35]
                newCar.dealerpricecombo = row[36]
                newCar.kess = row[37]
                newCar.ktag = row[38]
                db.session.commit()

                # for item in row:
                #     # print(item)
                #     # print(attr)
                #     # print(itemLoop)

                #     attr = header[itemLoop]
                #     newCar.originalpw = item
                #     itemLoop += 1
                #     # print(attr, item, type(attr), type(item))
                # idLoop += 1

            # for car in autosQ:
            #     print(car.originalpw)
            flash('Base de datos actualizada', category='success')
    return render_template('add.html', user=current_user)
