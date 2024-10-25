from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(400), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    stock = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return f'<Products {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
        }
    
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    
    # Representación del objeto
    def __repr__(self):
        return f'<Categoria {self.name}>'

    # Método para serializar el objeto
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


    # Método para serializar los datos de la categoría

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(80), unique=False, nullable=False)
    bank_account = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Seller {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone" : self.phone,
        }
    
class Comprador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    clave = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.String(80), unique=False, nullable=False)
        
     
        # Representación del objeto
    def __repr__(self):
        return f'<Comprador {self.name} '

    # Método para serializar los datos del comprador
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "clave": self.clave,
            "telefono": self.telefono
        }


   
    
        
     
   
      
        

