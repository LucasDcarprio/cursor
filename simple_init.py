"""
简化的数据库初始化脚本
"""
import os
import sys
sys.path.append('.')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# 简化的Flask应用配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 简化的用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    brand_name = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    store_id = db.Column(db.String(100), nullable=False)
    alibaba_openid = db.Column(db.String(100))
    alibaba_openkey = db.Column(db.String(100))
    alibaba_token = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')
    expire_time = db.Column(db.DateTime)
    max_stores = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据表创建完成")
        
        # 检查是否已存在超级管理员
        super_admin = User.query.filter_by(role='super').first()
        if super_admin:
            print(f"超级管理员已存在: {super_admin.username}")
            return
        
        # 创建超级管理员用户
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            phone='13800138000',
            brand_name='泓枢智创',
            store_name='总部',
            store_id='HQ001',
            role='super',
            max_stores=999,
            expire_time=datetime.utcnow() + timedelta(days=3650)
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("超级管理员用户创建成功:")
        print("用户名: admin")
        print("密码: admin123")
        print("角色: super")
        print("请登录后立即修改默认密码!")

if __name__ == '__main__':
    init_database()