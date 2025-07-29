"""
API视图 - RESTful接口，支持外部应用访问
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
import jwt
from datetime import datetime, timedelta

from app import db
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.order import Order

api_bp = Blueprint('api', __name__)

def api_response(data=None, message='success', code=200):
    """标准API响应格式"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }), code

def require_api_auth(f):
    """API认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return api_response(message='缺少认证令牌', code=401)
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            # 验证JWT令牌
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.query.get(user_id)
            
            if not user:
                return api_response(message='用户不存在', code=401)
            
            if user.is_expired():
                return api_response(message='账户已过期', code=401)
            
            # 将用户信息添加到请求上下文
            request.current_user = user
            
        except jwt.ExpiredSignatureError:
            return api_response(message='令牌已过期', code=401)
        except jwt.InvalidTokenError:
            return api_response(message='无效令牌', code=401)
        
        return f(*args, **kwargs)
    return decorated

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API登录接口"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return api_response(message='用户名和密码不能为空', code=400)
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        if user.is_expired():
            return api_response(message='账户已过期', code=401)
        
        # 生成JWT令牌
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return api_response(data={
            'token': token,
            'user': user.to_dict()
        }, message='登录成功')
    
    return api_response(message='用户名或密码错误', code=401)

@api_bp.route('/users/profile', methods=['GET'])
@require_api_auth
def get_profile():
    """获取用户资料"""
    return api_response(data=request.current_user.to_dict())

@api_bp.route('/stores', methods=['GET'])
@require_api_auth
def get_stores():
    """获取门店列表"""
    user = request.current_user
    
    query = Store.query
    if not user.is_super():
        query = query.filter_by(from_user=user.id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    if search:
        query = query.filter(Store.store_name.contains(search))
    
    stores = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return api_response(data={
        'stores': [store.to_dict() for store in stores.items],
        'total': stores.total,
        'pages': stores.pages,
        'current_page': page
    })

@api_bp.route('/stores', methods=['POST'])
@require_api_auth
def create_store():
    """创建门店"""
    user = request.current_user
    
    # 检查是否可以添加门店
    if not user.is_super() and not user.can_add_store():
        return api_response(message='已达到最大门店数量限制', code=403)
    
    data = request.get_json()
    
    if not data or not data.get('store_id') or not data.get('store_name'):
        return api_response(message='门店ID和名称为必填字段', code=400)
    
    # 检查门店ID唯一性
    if Store.query.filter_by(store_id=data['store_id']).first():
        return api_response(message='门店ID已存在', code=400)
    
    try:
        store = Store(
            store_id=data['store_id'],
            store_name=data['store_name'],
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            mobile=data.get('mobile', ''),
            contact_name=data.get('contact_name', ''),
            province=data.get('province', ''),
            city=data.get('city', ''),
            district=data.get('district', ''),
            postcode=data.get('postcode', ''),
            district_code=data.get('district_code', ''),
            alibaba_openid=data.get('alibaba_openid', ''),
            alibaba_openkey=data.get('alibaba_openkey', ''),
            alibaba_token=data.get('alibaba_token', ''),
            from_user=user.id
        )
        
        db.session.add(store)
        db.session.commit()
        
        return api_response(data=store.to_dict(), message='门店创建成功')
        
    except Exception as e:
        db.session.rollback()
        return api_response(message=f'创建失败：{str(e)}', code=500)

@api_bp.route('/products', methods=['GET'])
@require_api_auth
def get_products():
    """获取商品列表"""
    user = request.current_user
    
    query = Product.query
    if not user.is_super():
        query = query.filter_by(from_user=user.id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    if search:
        query = query.filter(Product.product_name.contains(search))
    
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return api_response(data={
        'products': [product.to_dict() for product in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': page
    })

@api_bp.route('/products', methods=['POST'])
@require_api_auth
def create_product():
    """创建商品"""
    user = request.current_user
    data = request.get_json()
    
    if not data or not data.get('product_name'):
        return api_response(message='商品名称为必填字段', code=400)
    
    try:
        product = Product(
            barcode=data.get('barcode', ''),
            sku_code=data.get('sku_code', ''),
            product_name=data['product_name'],
            specification=data.get('specification', ''),
            purchase_attributes=data.get('purchase_attributes', ''),
            settlement_link=data.get('settlement_link', ''),
            unit_count=data.get('unit_count', ''),
            min_order=data.get('min_order', ''),
            meituan_price=data.get('meituan_price', ''),
            manufacturer=data.get('manufacturer', ''),
            from_user=user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        return api_response(data=product.to_dict(), message='商品创建成功')
        
    except Exception as e:
        db.session.rollback()
        return api_response(message=f'创建失败：{str(e)}', code=500)

@api_bp.route('/orders', methods=['GET'])
@require_api_auth
def get_orders():
    """获取订单列表"""
    user = request.current_user
    
    query = Order.query
    if not user.is_super():
        query = query.filter_by(from_user=user.id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    
    if search:
        query = query.filter(Order.product_name.contains(search))
    
    if status:
        query = query.filter_by(order_status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return api_response(data={
        'orders': [order.to_dict() for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page
    })

@api_bp.route('/orders', methods=['POST'])
@require_api_auth
def create_order():
    """创建订单"""
    user = request.current_user
    data = request.get_json()
    
    if not data or not data.get('store_id') or not data.get('items'):
        return api_response(message='门店ID和商品项为必填字段', code=400)
    
    try:
        orders = []
        for item in data['items']:
            order = Order(
                store_id=data['store_id'],
                product_name=item.get('product_name', ''),
                sku_code=item.get('sku_code', ''),
                purchase_quantity=str(item.get('quantity', 0)),
                purchase_price=str(item.get('price', 0)),
                supplier=item.get('supplier', ''),
                order_status='pending',
                from_user=user.id
            )
            db.session.add(order)
            orders.append(order)
        
        db.session.commit()
        
        return api_response(
            data=[order.to_dict() for order in orders],
            message='订单创建成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(message=f'创建失败：{str(e)}', code=500)

@api_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@require_api_auth
def update_order_status(order_id):
    """更新订单状态"""
    user = request.current_user
    data = request.get_json()
    
    if not data or not data.get('status'):
        return api_response(message='状态为必填字段', code=400)
    
    order = Order.query.get_or_404(order_id)
    
    # 检查权限
    if not order.can_access(user):
        return api_response(message='权限不足', code=403)
    
    try:
        order.order_status = data['status']
        if data.get('reason'):
            order.failure_reason = data['reason']
        
        db.session.commit()
        
        return api_response(data=order.to_dict(), message='状态更新成功')
        
    except Exception as e:
        db.session.rollback()
        return api_response(message=f'更新失败：{str(e)}', code=500)

@api_bp.route('/stats', methods=['GET'])
@require_api_auth
def get_stats():
    """获取统计数据"""
    user = request.current_user
    
    stats = {}
    
    if user.is_super():
        # 超级管理员看到所有数据
        stats['total_users'] = User.query.count()
        stats['total_stores'] = Store.query.count()
        stats['total_products'] = Product.query.count()
        stats['total_orders'] = Order.query.count()
    else:
        # 普通用户只看到自己的数据
        stats['total_stores'] = Store.query.filter_by(from_user=user.id).count()
        stats['total_products'] = Product.query.filter_by(from_user=user.id).count()
        stats['total_orders'] = Order.query.filter_by(from_user=user.id).count()
    
    return api_response(data=stats)