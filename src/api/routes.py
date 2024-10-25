"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Products, Seller , Comprador,Categoria, ItemCart,Direccion
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#---------products-----------
@api.route('/products', methods=['GET'])
def get_products():
    products = Products.query.all()
    
    products = list(map(lambda product: product.serialize(), products))
    
    return jsonify(products), 200

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.get(product_id)

    if product is None:
        return jsonify({"message": "Product not found"}), 404
    
    return jsonify(product.serialize()), 200

@api.route('/products', methods=['POST'])
def add_product():
    new_product_data = request.get_json()

    if not new_product_data:
        return jsonify({"error": "No data provided for the new product."}), 400
    
    required_fields = ["name", "description", "price", "stock", "image"]
    if not all(field in new_product_data for field in required_fields):
        return jsonify({"error": "Required fields are missing: " + ', '.join(required_fields)}), 400
    
    if not isinstance(new_product_data["price"], (int, float)) or new_product_data["price"] < 0:
        return jsonify({"error": "The price must be a non-negative integer."}), 400
    
    if not isinstance(new_product_data["stock"], int) or new_product_data["stock"] < 0:
        return jsonify({"error": "The stock must be a non-negative integer."}), 400
    
    new_product = Products(
        name=new_product_data["name"],
        description=new_product_data["description"],
        price=new_product_data["price"],
        stock=new_product_data["stock"],
        image=new_product_data["image"]
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message":"Product successfully added"}), 201

@api.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):

    product = Products.query.get(product_id)

    if not product:
        return jsonify({"message":"Product no found"}), 404

    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Product successfully removed"}), 200

@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    product = Products.query.get(product_id)

    if product is None:
        return jsonify({"error": "Producto no encontrado."}), 404

   
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data has been provided for updating."}), 400

    if data["stock"]:
        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return jsonify({"message":"The stock must be a non-negative integer."}), 400
    product.stock = data['stock']

    if data["price"]:
        if not isinstance(data["price"], int) or data["price"] < 0:
            return jsonify({"message":"The price must be a non-negative integer."}), 400
    product.price = data['price']

    # Actualiza directamente los campos del producto
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'image' in data:
        product.image = data['image']

    db.session.commit()
    
    return jsonify({"message":"Product successfully edited"}), 200

#--------buyer----------------------------------------------


@api.route('/categoria', methods=['GET'])
def get_categoria():
    categorias = Categoria.query.all()  # Obtiene todas las categorías de la base de datos
    return jsonify([categoria.serialize() for categoria in categorias]), 200  # Devuelve las categorías en formato JSON

@api.route('/categoria/<int:categoria_id>', methods=['GET'])
def get_categoria_by_id(categoria_id):
    categoria = Categoria.query.get(categoria_id)  # Obtiene la categoría por ID
    if not categoria:
        return jsonify({"message": "Categoría no encontrada"}), 404  # Si no se encuentra, devuelve 404
    return jsonify(categoria.serialize()), 200  # Devuelve la categoría en formato JSON si la encuentra

@api.route('/categoria', methods=['POST'])
def add_categoria():
    new_categoria_data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud

    if not new_categoria_data:  # Verifica que se haya enviado algún dato
        return jsonify({"error": "No se han proporcionado datos"}), 400  # Si no se envía dato, devuelve error 400

    # Verifica que los campos requeridos estén presentes
    required_fields = ["name"]
    if not all(field in new_categoria_data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos: " + ', '.join(required_fields)}), 400  # Si falta algún campo, devuelve error 400

    # Crea una nueva categoría
    new_categoria = Categoria(
        name=new_categoria_data["name"],
    )

    # Guarda la nueva categoría en la base de datos
    db.session.add(new_categoria)
    db.session.commit()

    return jsonify({"message": "Categoría añadida exitosamente"}), 201  # Devuelve mensaje de éxito con código 201

@api.route('/categoria/<int:categoria_id>', methods=['PUT'])
def update_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)  # Obtiene la categoría por ID

    if categoria is None:
        return jsonify({"error": "Categoría no encontrada"}), 404  # Si no se encuentra, devuelve error 404

    data = request.get_json()  # Obtiene los datos de la solicitud

    if not data:  # Verifica que los datos no estén vacíos
        return jsonify({"error": "No se han proporcionado datos para actualizar"}), 400  # Si no hay datos, devuelve error 400

    # Actualiza los campos solo si fueron proporcionados en la solicitud
    if 'name' in data:
        categoria.name = data['name']
   
    db.session.commit()  # Guarda los cambios en la base de datos

    return jsonify({"message": "Categoría actualizada exitosamente"}), 200  # Devuelve mensaje de éxito

@api.route('/categoria/<int:categoria_id>', methods=['DELETE'])
def remove_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)  # Obtiene la categoría por ID

    if categoria is None:
        return jsonify({"error": "Categoría no encontrada"}), 404  # Devuelve un error 404 si no se encuentra la categoría

    db.session.delete(categoria)  # Elimina la categoría de la base de datos
    db.session.commit()  # Confirma la transacción

    return jsonify({"message": "Categoría eliminada exitosamente"}), 200  # Devuelve un mensaje de éxito

#----------------------------------Endpoints de Comprador-------------------------------------------

@api.route('/compradores', methods=['GET'])
def get_compradores():
    compradores = Comprador.query.all()  # Obtiene todos los compradores de la base de datos
    return jsonify([comprador.serialize() for comprador in compradores]), 200  # Devuelve los compradores en formato JSON

@api.route('/compradores/<int:comprador_id>', methods=['GET'])
def get_comprador(comprador_id):
    comprador = Comprador.query.get(comprador_id)  # Obtiene el comprador por ID
    if not comprador:
        return jsonify({"message": "Comprador no encontrado"}), 404  # Si no se encuentra, devuelve 404
    return jsonify(comprador.serialize()), 200  # Devuelve el comprador en formato JSON si lo encuentra

@api.route('/compradores', methods=['POST'])
def add_comprador():
    new_comprador_data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud

    if not new_comprador_data:  # Verifica que se haya enviado algún dato
        return jsonify({"error": "No data provided"}), 400  # Si no se envía dato, devuelve error 400

    # Verifica que los campos requeridos estén presentes
    required_fields = ["name", "email", "clave", "telefono"]
    if not all(field in new_comprador_data for field in required_fields):
        return jsonify({"error": "Required fields are missing: " + ', '.join(required_fields)}), 400  # Si falta algún campo, devuelve error 400

    # Verifica si ya existe un comprador con el mismo email
    existing_comprador = Comprador.query.filter_by(email=new_comprador_data["email"]).first()
    if existing_comprador:
        return jsonify({"error": "Email is already in use"}), 400  # Si el email ya está en uso, devuelve error 400

    # Crea un nuevo comprador
    new_comprador = Comprador(
        name=new_comprador_data["name"],
        email=new_comprador_data["email"],
        clave=new_comprador_data["clave"],
        telefono=new_comprador_data["telefono"]
    )

    # Guarda el nuevo comprador en la base de datos
    db.session.add(new_comprador)
    db.session.commit()

    return jsonify({"message": "Comprador successfully added"}), 201  # Devuelve mensaje de éxito con código 201

@api.route('/compradores/<int:comprador_id>', methods=['PUT'])
def update_comprador(comprador_id):
    comprador = Comprador.query.get(comprador_id)  # Obtiene el comprador por ID

    if comprador is None:
        return jsonify({"error": "Comprador no encontrado"}), 404  # Si no se encuentra, devuelve error 404

    data = request.get_json()  # Obtiene los datos de la solicitud

    if not data:  # Verifica que los datos no estén vacíos
        return jsonify({"error": "No data has been provided for updating"}), 400  # Si no hay datos, devuelve error 400

    # Actualiza los campos solo si fueron proporcionados en la solicitud
    if 'name' in data:
        comprador.name = data['name']
    if 'email' in data:
        comprador.email = data['email']
    if 'clave' in data:
        comprador.clave = data['clave']
    if 'telefono' in data:
        comprador.telefono = data['telefono']

    db.session.commit()  # Guarda los cambios en la base de datos

    return jsonify({"message": "Comprador successfully updated"}), 200  # Devuelve mensaje de éxito

@api.route('/compradores/<int:comprador_id>', methods=['DELETE'])
def remove_comprador(comprador_id):
    comprador = Comprador.query.get(comprador_id)  # Obtiene el comprador por ID

    if comprador is None:
        return {"error": "Comprador no encontrado"}, 404  # Devuelve un error 404 si no se encuentra el comprador

    db.session.delete(comprador)  # Elimina el comprador de la base de datos
    db.session.commit()  # Confirma la transacción

    return {"message": "Comprador eliminado exitosamente"}, 200  # Devuelve un mensaje de éxito

#-------------------seller----------------------------------------
@api.route('/sellers', methods=['GET'])
def get_sellers():
    sellers = Seller.query.all()
    
    sellers = list(map(lambda seller: seller.serialize(), sellers))
    
    return jsonify(sellers), 200

@api.route('/seller/<int:seller_id>', methods=['GET'])
def get_seller(seller_id):
    seller = Seller.query.get(seller_id)
    if not seller:
        return jsonify({"msg": "Vendedor no encontrado"}), 404
    return jsonify(seller.serialize()), 200


@api.route('/seller/signup', methods=['POST'])
def signup():
    body = request.get_json()

    if not body or not body.get("email") or not body.get("password"):
        return jsonify({"msg": "Email y contraseña son requeridos"}), 400

    seller = Seller.query.filter_by(email=body["email"]).first()

    if seller is not None:
        return jsonify({"msg": "El usuario ya existe"}), 409

    new_seller = Seller(
        email=body["email"],
        password =body["password"],
        phone=body["phone"],
        bank_account=body["bank_account"],
        is_active=True)
     

    db.session.add(new_seller)
    db.session.commit()

    
    return jsonify({"msg": "Usuario creado exitosamente"}), 200


@api.route('/seller/<int:seller_id>', methods=['DELETE'])
def delete_seller(seller_id):
    seller = Seller.query.get(seller_id)
    
    if not seller :
        return jsonify({"msg": "No autorizado o vendedor no encontrado"}), 403

    db.session.delete(seller)
    db.session.commit()
    return jsonify({"msg": "Vendedor eliminado"}), 200

@api.route('/seller/<int:seller_id>', methods=['PUT'])
def update_seller(seller_id):

    seller = Seller.query.get(seller_id)

    if seller is None:
        return jsonify({"error": "vendedor no existe."}), 404

   
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data has been provided for updating."}), 400

   
    if 'email' in data:
        seller.email = data['email']
    if 'password' in data:
        seller.password = data['password']
    if 'phone' in data:
        seller.phone = data['phone']
    if 'bank_account' in data:
        seller.bank_account = data['bank_account']

    db.session.commit()
    
    return jsonify({"msg":"vendedor actualizado"}), 200

#-------------itemcart-------------------------


@api.route('/itemscarts', methods=['GET'])
def get_itemscarts():
    carts = ItemCart.query.all()
    
    carts = list(map(lambda cart: cart.serialize(), carts))
    
    return jsonify(carts), 200

@api.route('/itemscarts/<int:itemcart_id>', methods=['GET'])
def get_itemcart(itemcart_id):
    item_cart = ItemCart.query.get(itemcart_id)
    if item_cart is None:
        return jsonify({"message": "Product not found"}), 404
    
    return jsonify(item_cart.serialize()), 200

@api.route('/itemscarts', methods=['POST'])
def add_itemcart():
    new_item_cart_data = request.get_json()

    if not new_item_cart_data:
        return jsonify({"error": "No data provided for the new item cart."}), 400
    
    
    if "amount" not in new_item_cart_data:
        return jsonify({"error": "you have to enter an amount"}), 400
    
    if not isinstance(new_item_cart_data["amount"], int) or new_item_cart_data["amount"] < 1:
        return jsonify({"error": "The amount must be a non-negative integer."}), 400
    
    new_product = ItemCart(
        amount=new_item_cart_data["amount"]
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message":"Product successfully added"}), 201

@api.route('/itemscarts/<int:itemcart_id>', methods=['DELETE'])
def remove_itemcart(itemcart_id):

    itemcart = ItemCart.query.get(itemcart_id)

    if not itemcart:
        return jsonify({"message":"itemcart no found"}), 404

    db.session.delete(itemcart)
    db.session.commit()
    
    return jsonify({"message": "itemcart successfully removed"}), 200

@api.route('/itemscarts/<int:itemcart_id>', methods=['PUT'])
def update_itemcart(itemcart_id):

    itemcart = ItemCart.query.get(itemcart_id)

    if itemcart is None:
        return jsonify({"error": "itemcart no found."}), 404

    data = request.get_json()

    if not data["amount"]:
        return jsonify({"error": "No data has been provided for updating."}), 400

    if not isinstance(data["amount"], int) or data["amount"] < 1:
        return jsonify({"message":"The amount must be a non-negative integer."}), 400

    itemcart.amount = data["amount"]

    db.session.commit()
    
    return jsonify({"message":"itemcart successfully edited"}), 200


#------------------LOGINBUYERS---------------

@api.route("/buyer/signup", methods = ['POST'])
def signupBuyer():
    new_comprador_data = request.get_json() 

    if not new_comprador_data: 
        return jsonify({"error": "No data provided"}), 400  
  
    required_fields = ["name", "email", "clave", "telefono"]
    if not all(field in new_comprador_data for field in required_fields):
        return jsonify({"error": "Required fields are missing: " + ', '.join(required_fields)}), 400  

    existing_comprador = Comprador.query.filter_by(email=new_comprador_data["email"]).first()
    if existing_comprador:
        return jsonify({"error": "Email is already in use"}), 400

    new_comprador = Comprador(
        name=new_comprador_data["name"],
        email=new_comprador_data["email"],
        clave=new_comprador_data["clave"],
        telefono=new_comprador_data["telefono"]
    )

    db.session.add(new_comprador)
    db.session.commit()

    return jsonify({"message": "Comprador successfully added"}), 201


@api.route("/buyer/login", methods=["POST"])
def loginbuyer():
    email = request.json.get("email")
    clave = request.json.get("clave")
    comprador = Comprador.query.filter_by(email = email, clave = clave).first()

    if comprador is None or clave != comprador.clave:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity= comprador.id)

    return jsonify(access_token=access_token), 200

#///////////////////////////Address

@api.route('/direcciones', methods=['GET'])
def get_direcciones():
    direcciones = Address.query.all()
    return jsonify([direccion.serialize() for direccion in direcciones]), 200

@api.route('/direcciones/<int:direccion_id>', methods=['GET'])
def get_direccion(direccion_id):
    direccion = Address.query.get(direccion_id)
    if not direccion:
        return jsonify({"message": "Direccion no encontrado"}), 404
    return jsonify(direccion.serialize()), 200

@api.route('/direcciones', methods=['POST'])
def add_direccion():
    new_direccion_data = request.get_json()

    if not new_direccion_data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["direccion", "ciudad", "codigo_postal", "pais"]
    if not all(field in new_direccion_data for field in required_fields):
        return jsonify({"error": "Required fields are missing: " + ', '.join(required_fields)}), 400
    
    new_direccion = Address(
        direccion=new_direccion_data["direccion"],
        ciudad=new_direccion_data["ciudad"],
        codigo_postal=new_direccion_data["codigo_postal"],
        pais=new_direccion_data["pais"]
    )

    db.session.add(new_direccion)
    db.session.commit()

    return jsonify({"message": "Direccion successfully added"}), 201

@api.route('/direcciones/<int:direccion_id>', methods=['PUT'])
def update_direccion(direccion_id):
    direccion = Address.query.get(direccion_id)

    if direccion is None:
        return jsonify({"error": "Direccion no encontrado"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data has been provided for updating"}), 400

    if 'direccion' in data:
        direccion.direccion = data['direccion']
    if 'ciudad' in data:
        direccion.ciudad = data['ciudad']
    if 'codigo_postal' in data:
        direccion.codigo_postal = data['codigo_postal']
    if 'pais' in data:
        direccion.pais = data['pais']

    db.session.commit()

    return jsonify({"message": "Direccion successfully updated"}), 200

@api.route('/direcciones/<int:direccion_id>', methods=['DELETE'])
def remove_direccion(direccion_id):
    direccion = Address.query.get(direccion_id)

    if direccion is None:
        return {"error": "Direccion no encontrado"}, 404

    db.session.delete(direccion)
    db.session.commit()

    return {"message": "Direccion eliminado exitosamente"}, 200

