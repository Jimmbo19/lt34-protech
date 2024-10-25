  
import os
from flask_admin import Admin
from .models import db, User, Products,Seller, Comprador, ItemCart, Categoria, Cart, Direccion
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Products, db.session))
    admin.add_view(ModelView(Categoria, db.session))
    admin.add_view(ModelView(Seller, db.session))
    admin.add_view(ModelView(Comprador, db.session))
    admin.add_view(ModelView(ItemCart, db.session))
    admin.add_view(ModelView(Cart, db.session))
    admin.add_view(ModelView(Direccion, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))