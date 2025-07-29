"""
用户模型 - 支持多角色权限管理
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(256), nullable=False)  # 密码哈希
    phone = db.Column(db.String(20), nullable=False)  # 手机号
    brand_name = db.Column(db.String(100), nullable=False)  # 品牌名称
    store_name = db.Column(db.String(100), nullable=False)  # 店铺名称
    store_id = db.Column(db.String(100), nullable=False)  # 店铺ID
    
    # 阿里巴巴API凭证
    alibaba_openid = db.Column(db.String(100))
    alibaba_openkey = db.Column(db.String(100))
    alibaba_token = db.Column(db.String(100))
    
    # 角色和权限
    role = db.Column(db.String(20), default='user')  # user, admin, super
    
    # 租户管理字段(super用户可控制)
    expire_time = db.Column(db.DateTime)  # 到期时间
    max_stores = db.Column(db.Integer, default=1)  # 最大门店数量
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_super(self):
        """是否为超级管理员"""
        return self.role == 'super'
    
    def is_admin(self):
        """是否为管理员"""
        return self.role in ['admin', 'super']
    
    def is_expired(self):
        """检查是否过期"""
        if not self.expire_time:
            return False
        return datetime.utcnow() > self.expire_time
    
    def can_add_store(self):
        """检查是否可以添加门店"""
        from .store import Store
        current_count = Store.query.filter_by(from_user=self.id).count()
        return current_count < self.max_stores
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'brand_name': self.brand_name,
            'store_name': self.store_name,
            'store_id': self.store_id,
            'role': self.role,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'max_stores': self.max_stores,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'