from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from flask_cors import CORS
from datetime import timedelta
from flask_restful import Api, Resource
from flask_caching import Cache
import redis

app = Flask(__name__)
api = Api(app)
CORS(app, origins='*')

redis_client=redis.Redis(host='localhost',port=6379,db=0)

cache = Cache(app,config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': 'redis_client'})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisismysecretkey'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    confirmPassword = db.Column(db.String(80), nullable=False)
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"Categories(id={self.id}, name='{self.name}')"
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(50), nullable=False)
    manufacture_date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', category='{self.category}')"

def create_tables():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            name='Admin',
            username='admin',
            password=generate_password_hash('admin'),
            email='admin@example.com',
            role='admin',
            confirmPassword=generate_password_hash('admin'),
        )
        db.session.add(admin_user)
        db.session.commit()

with app.app_context():
    create_tables()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    confirm_password = data.get('confirmPassword')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    user = User(
        name=name,
        username=username,
        password=generate_password_hash(password),
        confirmPassword=generate_password_hash(confirm_password),
        email=email,
        role='user',
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=1))
    isauticated=True
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role,
    }

    return jsonify({'access_token': access_token, 'user': user_info}), 200

class CategoriesList(Resource):
    @cache.cached(timeout=2)
    @jwt_required()

    def get(self, category_id=None):
        if category_id is None:
            categories = Categories.query.all()
            category_list = [{'id': category.id, 'name': category.name} for category in categories]
            return jsonify(category_list)
        else:
            category = Categories.query.get(category_id)
            if category:
                return jsonify({'id': category.id, 'name': category.name})
            else:
                return jsonify({'error': 'Category not found'}), 404

    def post(self):
        data = request.get_json()
        category_name = data.get('name')
        if not category_name:
            return jsonify({'error': 'Category name is required'}), 400
        new_category = Categories(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return {'message': 'Category created successfully'}, 201

    def put(self, category_id):
        if not category_id:
            return jsonify({'error': 'Category ID is required'}), 400
        category = Categories.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        data = request.get_json()
        new_category_name = data.get('name')
        if not new_category_name:
            return jsonify({'error': 'Category name is required'}), 400
        category.name = new_category_name
        db.session.commit()
        return {'message': 'Category updated successfully'}, 200
    def delete(self, category_id):
        if not category_id:
            return jsonify({'error': 'Category ID is required'}), 400
        category = Categories.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}, 200
    

class ProductList(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        product_name = data.get('name')
        expiry_date = data.get('expiry_date')
        manufacture_date = data.get('manufacture_date')
        category = data.get('category')
        price = data.get('price')
        unit = data.get('unit')
        quantity = data.get('quantity')

        if not all([product_name, expiry_date, manufacture_date, category, price, unit, quantity]):
            return jsonify({'error': 'All fields are required'}), 400

        new_product = Product(
            name=product_name,
            expiry_date=expiry_date,
            manufacture_date=manufacture_date,
            category=category,
            price=price,
            unit=unit,
            quantity=quantity
        )
        db.session.add(new_product)
        db.session.commit()
        return {'message': 'Product added successfully'}, 201


api.add_resource(ProductList, '/products', '/products/<int:product_id>')
api.add_resource(CategoriesList, '/categories', '/categories/<int:category_id>')
@app.route('/api/customer/<int:user_id>/search', methods=['POST'])
def search_product(user_id):
    search_query = request.json.get('searchQuery', '')

    try:
        # Attempt to convert the search query to a float for price-based search
        price = float(search_query)
        products = Product.query.filter(Product.price == price).all()
    except ValueError:
        # If conversion fails, perform a name-based search
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
    
    # Prepare the response data
    product_list = [{
        'id': product.id,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'manufactureDate': product.manufacture_date.strftime('%Y-%m-%d'),
        'available': product.available,
        'quantity': product.quantity
    } for product in products]

    return jsonify(product_list), 200

if __name__ == '__main__':
    app.run(debug=True)