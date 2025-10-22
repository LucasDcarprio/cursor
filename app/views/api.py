"""
API 视图模块
API Views Module

提供 RESTful API 接口，支持外部系统集成。
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.order import Order
from app.extensions import db
from functools import wraps
import jwt
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

def token_required(f):
    """API Token 验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API 登录"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 401
        
        if user.is_expired():
            return jsonify({'error': 'Account has expired'}), 401
        
        # 生成 JWT Token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/stores', methods=['GET'])
@token_required
def api_get_stores(current_user):
    """获取门店列表"""
    stores = Store.query.filter_by(from_user=current_user.username).all()
    return jsonify({
        'stores': [store.to_dict() for store in stores]
    }), 200

@api_bp.route('/stores', methods=['POST'])
@token_required
def api_create_store(current_user):
    """创建门店"""
    data = request.get_json()
    
    if not data or not data.get('store_id') or not data.get('store_name'):
        return jsonify({'error': 'Store ID and name are required'}), 400
    
    # 检查门店ID是否已存在
    if Store.query.filter_by(store_id=data['store_id']).first():
        return jsonify({'error': 'Store ID already exists'}), 400
    
    store = Store(
        store_id=data['store_id'],
        store_name=data['store_name'],
        address=data.get('address', ''),
        province=data.get('province', ''),
        city=data.get('city', ''),
        district=data.get('district', ''),
        phone=data.get('phone', ''),
        mobile=data.get('mobile', ''),
        contact_name=data.get('contact_name', ''),
        from_user=current_user.username
    )
    
    db.session.add(store)
    db.session.commit()
    
    return jsonify({
        'message': 'Store created successfully',
        'store': store.to_dict()
    }), 201

@api_bp.route('/products', methods=['GET'])
@token_required
def api_get_products(current_user):
    """获取商品列表"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(from_user=current_user.username)
    
    if search:
        query = query.filter(
            db.or_(
                Product.product_name.contains(search),
                Product.sku_code.contains(search),
                Product.manufacturer.contains(search)
            )
        )
    
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'pagination': {
            'page': products.page,
            'pages': products.pages,
            'per_page': products.per_page,
            'total': products.total
        }
    }), 200

@api_bp.route('/orders', methods=['GET'])
@token_required
def api_get_orders(current_user):
    """获取订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    status = request.args.get('status', '')
    
    query = Order.query.filter_by(from_user=current_user.username)
    
    if status:
        query = query.filter_by(order_status=status)
    
    orders = query.order_by(Order.created_at.desc())\
                  .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order.to_dict() for order in orders.items],
        'pagination': {
            'page': orders.page,
            'pages': orders.pages,
            'per_page': orders.per_page,
            'total': orders.total
        }
    }), 200

@api_bp.route('/orders', methods=['POST'])
@token_required
def api_create_order(current_user):
    """创建订单"""
    data = request.get_json()
    
    required_fields = ['store_id', 'sku_code', 'purchase_quantity', 'supplier']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    order = Order(
        store_id=data['store_id'],
        sku_code=data['sku_code'],
        product_name=data.get('product_name', ''),
        purchase_quantity=str(data['purchase_quantity']),
        purchase_price=str(data.get('purchase_price', 0)),
        supplier=data['supplier'],
        order_status=Order.STATUS_WAITING_ORDER,
        from_user=current_user.username
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    }), 201