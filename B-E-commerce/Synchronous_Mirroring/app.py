from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Activer CORS pour permettre les requêtes cross-origin

# Connexion à la base de données primaire
def get_primary_db():
    conn = sqlite3.connect('primary.db')
    conn.row_factory = sqlite3.Row
    return conn

# Connexion à la base de données secondaire
def get_secondary_db():
    conn = sqlite3.connect('secondary.db')
    conn.row_factory = sqlite3.Row
    return conn

# Écriture synchrone dans les deux bases de données
def sync_write(query, params):
    primary_conn = get_primary_db()
    secondary_conn = get_secondary_db()
    try:
        # Écriture dans la base de données primaire
        primary_conn.execute(query, params)
        primary_conn.commit()
        # Écriture dans la base de données secondaire
        secondary_conn.execute(query, params)
        secondary_conn.commit()
    except Exception as e:
        # En cas d'erreur, annuler les changements dans les deux bases
        primary_conn.rollback()
        secondary_conn.rollback()
        raise e
    finally:
        # Fermer les connexions
        primary_conn.close()
        secondary_conn.close()

# Route pour servir la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route pour obtenir tous les produits
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_primary_db()
    cursor = conn.cursor()
    category = request.args.get('category')
    in_stock = request.args.get('inStock')

    query = 'SELECT * FROM products'
    if category:
        query += f" WHERE category = '{category}'"
    if in_stock:
        query += ' AND inStock = 1' if category else ' WHERE inStock = 1'

    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

# Route pour obtenir un produit par son ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = get_primary_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(dict(product))

# Route pour ajouter un nouveau produit (écriture synchrone)
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    query = '''
        INSERT INTO products (name, description, price, category, inStock)
        VALUES (?, ?, ?, ?, ?)
    '''
    params = (
        new_product['name'], new_product['description'], new_product['price'],
        new_product['category'], new_product['inStock']
    )
    sync_write(query, params)
    return jsonify(new_product), 201

# Route pour mettre à jour un produit (écriture synchrone)
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    updated_product = request.get_json()
    query = '''
        UPDATE products
        SET name = ?, description = ?, price = ?, category = ?, inStock = ?
        WHERE id = ?
    '''
    params = (
        updated_product['name'], updated_product['description'], updated_product['price'],
        updated_product['category'], updated_product['inStock'], id
    )
    sync_write(query, params)
    return jsonify({'id': id, **updated_product})

# Route pour supprimer un produit (écriture synchrone)
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    query = 'DELETE FROM products WHERE id = ?'
    params = (id,)
    sync_write(query, params)
    return jsonify({'message': 'Product deleted successfully'})

# Route pour créer une commande
@app.route('/orders', methods=['POST'])
def create_order():
    order_details = request.get_json()
    conn = get_primary_db()
    cursor = conn.cursor()
    total_price = 0
    for item in order_details['items']:
        cursor.execute('SELECT price FROM products WHERE id = ?', (item['productId'],))
        product = cursor.fetchone()
        if product:
            total_price += product['price'] * item['quantity']
    cursor.execute('''
        INSERT INTO orders (userId, productId, quantity, totalPrice, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (order_details['userId'], order_details['productId'], order_details['quantity'], total_price, 'Pending'))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return jsonify({'orderId': order_id, 'totalPrice': total_price, 'status': 'Pending'})

# Route pour obtenir les commandes d'un utilisateur
@app.route('/orders/<int:userId>', methods=['GET'])
def get_orders(userId):
    conn = get_primary_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE userId = ?', (userId,))
    orders = cursor.fetchall()
    conn.close()
    return jsonify([dict(order) for order in orders])

# Route pour ajouter un produit au panier
@app.route('/cart/<int:userId>', methods=['POST'])
def add_to_cart(userId):
    cart_item = request.get_json()
    conn = get_primary_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cart (userId, productId, quantity)
        VALUES (?, ?, ?)
        ON CONFLICT(userId, productId) DO UPDATE SET quantity = quantity + ?
    ''', (userId, cart_item['productId'], cart_item['quantity'], cart_item['quantity']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added to cart successfully'})

# Route pour obtenir le panier d'un utilisateur
@app.route('/cart/<int:userId>', methods=['GET'])
def get_cart(userId):
    conn = get_primary_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart WHERE userId = ?', (userId,))
    cart_items = cursor.fetchall()
    conn.close()
    return jsonify([dict(item) for item in cart_items])

# Route pour supprimer un produit du panier
@app.route('/cart/<int:userId>/item/<int:productId>', methods=['DELETE'])
def remove_from_cart(userId, productId):
    conn = get_primary_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE userId = ? AND productId = ?', (userId, productId))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product removed from cart successfully'})

if __name__ == '__main__':
    app.run(debug=True)