import sqlite3

# Fonction pour initialiser une base de données
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Créer la table des produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            inStock BOOLEAN NOT NULL
        )
    ''')

    # Créer la table des commandes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            productId INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            totalPrice REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(productId) REFERENCES products(id)
        )
    ''')

    # Créer la table des paniers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            userId INTEGER NOT NULL,
            productId INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY(userId, productId),
            FOREIGN KEY(productId) REFERENCES products(id)
        )
    ''')

    # Insérer des données de test dans la table des produits
    products = [
        ("Laptop", "A high-performance laptop", 1200.00, "Electronics", True),
        ("Smartphone", "Latest model smartphone", 800.00, "Electronics", True),
        ("Headphones", "Noise-cancelling headphones", 150.00, "Electronics", True),
        ("Tablet", "Lightweight and portable tablet", 400.00, "Electronics", True),
        ("Smartwatch", "Fitness and health tracking", 250.00, "Electronics", True),
        ("Camera", "High-resolution DSLR camera", 900.00, "Electronics", False),
        ("Printer", "Wireless color printer", 200.00, "Electronics", True),
        ("Monitor", "27-inch 4K monitor", 350.00, "Electronics", True),
        ("Keyboard", "Mechanical gaming keyboard", 120.00, "Electronics", True),
        ("Mouse", "Wireless ergonomic mouse", 60.00, "Electronics", True),
        ("Book", "A best-selling novel", 20.00, "Books", True),
        ("Notebook", "Hardcover notebook", 15.00, "Books", True),
        ("Pen", "Ballpoint pen", 5.00, "Books", True),
        ("Chair", "Comfortable office chair", 100.00, "Furniture", False),
        ("Desk", "Adjustable standing desk", 300.00, "Furniture", True),
        ("Lamp", "LED desk lamp", 50.00, "Furniture", True),
        ("Sofa", "3-seater leather sofa", 700.00, "Furniture", True),
        ("Table", "Wooden dining table", 250.00, "Furniture", True),
        ("Bed", "Queen-sized bed frame", 500.00, "Furniture", True),
        ("Wardrobe", "Large wooden wardrobe", 400.00, "Furniture", True),
    ]
    cursor.executemany('''
        INSERT INTO products (name, description, price, category, inStock)
        VALUES (?, ?, ?, ?, ?)
    ''', products)

    # Insérer des données de test dans la table des commandes
    orders = [
        (1, 1, 1, 1200.00, "Pending"),
        (1, 2, 2, 1600.00, "Shipped"),
        (2, 3, 1, 150.00, "Delivered"),
        (2, 4, 1, 400.00, "Pending"),
        (3, 5, 1, 250.00, "Shipped"),
        (3, 6, 1, 900.00, "Pending"),
        (4, 7, 1, 200.00, "Delivered"),
        (4, 8, 1, 350.00, "Pending"),
        (5, 9, 1, 120.00, "Shipped"),
        (5, 10, 1, 60.00, "Delivered"),
    ]
    cursor.executemany('''
        INSERT INTO orders (userId, productId, quantity, totalPrice, status)
        VALUES (?, ?, ?, ?, ?)
    ''', orders)

    # Insérer des données de test dans la table des paniers
    cart_items = [
        (1, 1, 1),
        (1, 2, 2),
        (2, 3, 1),
        (2, 4, 1),
        (3, 5, 1),
        (3, 6, 1),
        (4, 7, 1),
        (4, 8, 1),
        (5, 9, 1),
        (5, 10, 1),
    ]
    cursor.executemany('''
        INSERT INTO cart (userId, productId, quantity)
        VALUES (?, ?, ?)
    ''', cart_items)

    # Sauvegarde des changements et fermeture de la connexion
    conn.commit()
    conn.close()

# Initialiser les deux bases de données
init_db('primary.db')
init_db('secondary.db')