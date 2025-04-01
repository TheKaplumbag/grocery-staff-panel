from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
db = SQLAlchemy(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] #Hash password in production
        user = User.query.filter_by(username=username, password=password).first() #Hash password in production
        if user:
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # In a real application, hash this.
    role = db.Column(db.String(20), nullable=False) # 'manager' or 'cashier'

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]
    return jsonify(product_list)

@app.route('/sales', methods=['POST'])
def record_sale():
    data = request.get_json()
    new_sale = Sale(product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({'message': 'Sale recorded successfully'})

@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = Inventory.query.all()
    inventory_list = [{'product_id': i.product_id, 'quantity': i.quantity} for i in inventory]
    return jsonify(inventory_list)

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], role=data['role']) #Hash password in production
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})
  
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    