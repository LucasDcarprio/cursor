#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧采购管理系统 - 主应用入口
Intelligent Procurement Management System - Main Application Entry

这是系统的主入口文件，负责初始化 Flask 应用并启动服务。

作者：泓枢智创团队
版本：1.0.0
"""

import os
import sys
from flask import Flask
from config import get_config, validate_config

def create_app():
    """创建 Flask 应用实例"""
    app = Flask(__name__)
    
    # 加载配置
    config_class = get_config()
    app.config.from_object(config_class)
    
    # 验证配置
    if not validate_config():
        print("配置验证失败，请检查 config.py 文件")
        sys.exit(1)
    
    # 初始化扩展
    from app.extensions import init_extensions
    init_extensions(app)
    
    # 注册蓝图
    from app.views import register_blueprints
    register_blueprints(app)
    
    # 创建数据库表
    with app.app_context():
        from app.models import db
        db.create_all()
    
    return app

def main():
    """主函数"""
    # 创建应用
    app = create_app()
    
    # 获取运行参数
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"智慧采购管理系统启动中...")
    print(f"访问地址: http://{host}:{port}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    
    # 启动应用
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()