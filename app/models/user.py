"""
用户模型
定义用户相关的数据结构和操作
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(256), nullable=False, comment='密码哈希')
    phone = db.Column(db.String(20), nullable=False, comment='手机号')
    brand_name = db.Column(db.String(100), nullable=False, comment='品牌名称')
    store_name = db.Column(db.String(100), nullable=False, comment='门店名称')
    store_id = db.Column(db.String(100), nullable=False, comment='门店ID')
    
    # 阿里巴巴API凭证
    alibaba_openid = db.Column(db.String(100), comment='阿里巴巴OpenID')
    alibaba_openkey = db.Column(db.String(100), comment='阿里巴巴OpenKey')
    alibaba_token = db.Column(db.String(100), comment='阿里巴巴Token')
    
    # 权限和状态
    role = db.Column(db.String(20), default='user', comment='用户角色：user/admin/super')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    expire_time = db.Column(db.DateTime, comment='到期时间')
    max_stores = db.Column(db.Integer, default=1, comment='最大门店数量')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_expired(self):
        """检查是否过期"""
        if self.expire_time is None:
            return False
        return datetime.utcnow() > self.expire_time
    
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
            'is_active': self.is_active,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'max_stores': self.max_stores,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'