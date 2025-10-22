"""
视图层包
Views Package

包含所有的视图函数和蓝图注册。
"""

from flask import Blueprint

def register_blueprints(app):
    """注册所有蓝图"""
    
    # 导入蓝图
    from .auth import auth_bp
    from .admin import admin_bp
    from .api import api_bp
    from .alibaba import alibaba_bp
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(alibaba_bp, url_prefix='/alibaba')
    
    # 注册主页路由
    @app.route('/')
    def index():
        return "智慧采购管理系统 - 欢迎使用！"