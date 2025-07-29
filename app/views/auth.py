"""
用户认证视图 - 注册、登录、权限管理
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db, login_manager
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """用户加载回调"""
    return User.query.get(int(user_id))

@auth_bp.route('/')
def home():
    """首页"""
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('请输入用户名和密码', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # 检查用户是否过期
            if user.is_expired():
                flash('账户已过期，请联系管理员', 'error')
                return render_template('login.html')
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # 登录用户
            login_user(user, remember=remember)
            
            # 设置session信息
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'欢迎回来，{user.username}！', 'success')
            
            # 根据角色重定向
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('admin.dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()
        brand_name = data.get('brand_name', '').strip()
        store_name = data.get('store_name', '').strip()
        store_id = data.get('store_id', '').strip()
        
        # 验证必填字段
        if not all([username, password, phone, brand_name, store_name, store_id]):
            flash('请填写所有必填字段', 'error')
            return render_template('register.html')
        
        # 验证用户名唯一性
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')
        
        # 验证手机号唯一性
        if User.query.filter_by(phone=phone).first():
            flash('手机号已被注册', 'error')
            return render_template('register.html')
        
        try:
            # 创建新用户
            user = User(
                username=username,
                phone=phone,
                brand_name=brand_name,
                store_name=store_name,
                store_id=store_id,
                role='user',  # 默认为普通用户
                max_stores=1  # 默认最多1个门店
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('注册成功！请登录', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'注册失败：{str(e)}', 'error')
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    session.clear()
    flash('已成功退出登录', 'info')
    return redirect(url_for('auth.home'))

@auth_bp.route('/profile')
@login_required
def profile():
    """用户资料"""
    return render_template('profile.html', user=current_user)

@auth_bp.route('/check_auth')
@login_required
def check_auth():
    """检查认证状态 - API接口"""
    return jsonify({
        'authenticated': True,
        'user': current_user.to_dict()
    })

# 权限装饰器
def require_role(role):
    """角色权限装饰器"""
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录', 'error')
                return redirect(url_for('auth.login'))
            
            if role == 'super' and not current_user.is_super():
                flash('权限不足', 'error')
                return redirect(url_for('admin.dashboard'))
            elif role == 'admin' and not current_user.is_admin():
                flash('权限不足', 'error')
                return redirect(url_for('admin.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_super(f):
    """超级管理员权限装饰器"""
    return require_role('super')(f)

def require_admin(f):
    """管理员权限装饰器"""
    return require_role('admin')(f)