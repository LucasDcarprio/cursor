"""
数据库初始化脚本 - 创建表结构和超级管理员用户
"""
from app import create_app, db
from app.models.user import User
from datetime import datetime, timedelta

def init_database():
    """初始化数据库"""
    app = create_app()
    
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
            phone='13800138000',
            brand_name='泓枢智创',
            store_name='总部',
            store_id='HQ001',
            role='super',
            max_stores=999,  # 超级管理员无门店限制
            expire_time=datetime.utcnow() + timedelta(days=3650)  # 10年有效期
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("超级管理员用户创建成功:")
        print("用户名: admin")
        print("密码: admin123")
        print("角色: super")
        print("请登录后立即修改默认密码!")

def create_demo_data():
    """创建演示数据"""
    app = create_app()
    
    with app.app_context():
        from app.models.store import Store
        from app.models.product import Product
        from app.models.order import Order
        
        # 获取超级管理员
        admin_user = User.query.filter_by(role='super').first()
        if not admin_user:
            print("请先运行初始化脚本创建超级管理员")
            return
        
        # 创建演示门店
        demo_store = Store(
            store_id='DEMO001',
            store_name='演示门店',
            address='上海市浦东新区张江高科技园区',
            phone='021-12345678',
            mobile='13800138001',
            contact_name='张经理',
            province='上海市',
            city='上海市',
            district='浦东新区',
            postcode='201203',
            from_user=admin_user.id
        )
        
        # 创建演示商品
        demo_products = [
            Product(
                sku_code='SKU001',
                product_name='可口可乐 330ml',
                specification='330ml/瓶',
                manufacturer='可口可乐公司',
                meituan_price='3.50',
                min_order='24',
                unit_count='24',
                from_user=admin_user.id
            ),
            Product(
                sku_code='SKU002',
                product_name='康师傅方便面',
                specification='100g/包',
                manufacturer='康师傅控股有限公司',
                meituan_price='4.50',
                min_order='12',
                unit_count='12',
                from_user=admin_user.id
            ),
            Product(
                sku_code='SKU003',
                product_name='农夫山泉 550ml',
                specification='550ml/瓶',
                manufacturer='农夫山泉股份有限公司',
                meituan_price='2.00',
                min_order='24',
                unit_count='24',
                from_user=admin_user.id
            )
        ]
        
        # 创建演示订单
        demo_orders = [
            Order(
                store_id='DEMO001',
                product_name='可口可乐 330ml',
                sku_code='SKU001',
                purchase_quantity='48',
                purchase_price='3.20',
                supplier='可口可乐经销商',
                order_status='pending',
                from_user=admin_user.id
            ),
            Order(
                store_id='DEMO001',
                product_name='康师傅方便面',
                sku_code='SKU002',
                purchase_quantity='24',
                purchase_price='4.00',
                supplier='康师傅经销商',
                order_status='processing',
                from_user=admin_user.id
            )
        ]
        
        try:
            # 添加演示数据
            db.session.add(demo_store)
            for product in demo_products:
                db.session.add(product)
            for order in demo_orders:
                db.session.add(order)
            
            db.session.commit()
            print("演示数据创建成功:")
            print("- 1个演示门店")
            print("- 3个演示商品")
            print("- 2个演示订单")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建演示数据失败: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        create_demo_data()
    else:
        init_database()
        
        # 询问是否创建演示数据
        create_demo = input("\n是否创建演示数据? (y/n): ").lower().strip()
        if create_demo in ['y', 'yes', '是']:
            create_demo_data()