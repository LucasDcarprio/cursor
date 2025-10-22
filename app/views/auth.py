"""
认证视图模块
Authentication Views Module

处理用户登录、注册、注销等认证相关功能。
"""

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('请输入用户名和密码', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('账户已被禁用，请联系管理员', 'error')
                return render_template('auth/login.html')
            
            if user.is_expired():
                flash('账户已过期，请联系管理员续费', 'error')
                return render_template('auth/login.html')
            
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'欢迎回来，{user.username}！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        brand_name = request.form.get('brand_name')
        store_name = request.form.get('store_name')
        store_id = request.form.get('store_id')
        
        # 验证必填字段
        if not all([username, password, phone, brand_name, store_name, store_id]):
            flash('请填写所有必填字段', 'error')
            return render_template('auth/register.html')
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('auth/register.html')
        
        # 创建新用户
        user = User(
            username=username,
            phone=phone,
            brand_name=brand_name,
            store_name=store_name,
            store_id=store_id
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """用户注销"""
    logout_user()
    flash('您已成功注销', 'info')
    return redirect(url_for('auth.login'))