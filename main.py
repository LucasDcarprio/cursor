"""
智慧采购管理系统 - 主入口文件
"""
from app import create_app

# 创建Flask应用实例
app = create_app()

if __name__ == '__main__':
    # 开发模式运行
    app.run(debug=True, host='0.0.0.0', port=5000)