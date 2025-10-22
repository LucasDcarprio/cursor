"""
管理后台视图模块
Admin Views Module

处理管理后台的各种功能，包括仪表板、数据管理等。
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.order import Order
from app.extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """管理后台首页"""
    # 获取统计数据
    stats = {
        'total_stores': Store.query.filter_by(from_user=current_user.username).count(),
        'total_products': Product.query.filter_by(from_user=current_user.username).count(),
        'total_orders': Order.query.filter_by(from_user=current_user.username).count(),
        'pending_orders': Order.query.filter_by(
            from_user=current_user.username, 
            order_status=Order.STATUS_WAITING_ORDER
        ).count()
    }
    
    # 获取最近的订单
    recent_orders = Order.query.filter_by(from_user=current_user.username)\
                              .order_by(Order.created_at.desc())\
                              .limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin_bp.route('/stores')
@login_required
def stores():
    """门店管理"""
    page = request.args.get('page', 1, type=int)
    stores = Store.query.filter_by(from_user=current_user.username)\
                       .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/stores.html', stores=stores)

@admin_bp.route('/products')
@login_required
def products():
    """商品管理"""
    page = request.args.get('page', 1, type=int)
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
    
    products = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/products.html', products=products, search=search)

@admin_bp.route('/orders')
@login_required
def orders():
    """订单管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query.filter_by(from_user=current_user.username)
    
    if status:
        query = query.filter_by(order_status=status)
    
    orders = query.order_by(Order.created_at.desc())\
                  .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/orders.html', orders=orders, status=status)

@admin_bp.route('/users')
@login_required
def users():
    """用户管理（仅超级管理员）"""
    if current_user.role != 'super':
        flash('权限不足', 'error')
        return redirect(url_for('admin.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users)