"""
Flask 扩展初始化模块
Flask Extensions Initialization Module

统一管理和初始化所有 Flask 扩展。
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 初始化扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_extensions(app):
    """初始化所有扩展"""
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化登录管理
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录后访问该页面。'
    login_manager.login_message_category = 'info'
    
    # 初始化数据库迁移
    migrate.init_app(app, db)
    
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    return app