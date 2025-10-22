"""
订单模型
定义采购订单相关的数据结构和操作
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    """采购订单模型"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 订单基本信息
    store_id = db.Column(db.String(100), comment='门店ID')
    product_name = db.Column(db.String(255), comment='商品名称')
    sku_code = db.Column(db.String(255), comment='SKU编码')
    
    # 采购信息
    purchase_quantity = db.Column(db.String(50), comment='采购量')
    purchase_price = db.Column(db.String(50), comment='采购单价')
    supplier = db.Column(db.String(100), comment='供应商')
    received_quantity = db.Column(db.String(50), comment='收货量')
    
    # 订单状态和处理
    order_status = db.Column(db.String(50), comment='订单状态')
    order_number = db.Column(db.String(100), comment='订单编号')
    purchase_order_number = db.Column(db.String(100), comment='采购单号')
    logistics_number = db.Column(db.String(100), comment='物流单号')
    
    # 支付信息
    actual_payment = db.Column(db.String(50), comment='实际支付')
    failure_reason = db.Column(db.Text, comment='失败原因')
    
    # 备注和预留字段
    remarks = db.Column(db.Text, comment='备注')
    reserved_0 = db.Column(db.String(255), comment='预留字段0')
    reserved_1 = db.Column(db.String(255), comment='预留字段1')
    reserved_2 = db.Column(db.String(255), comment='预留字段2')
    
    # 归属和权限
    from_user = db.Column(db.String(100), nullable=False, comment='归属用户')
    
    # 时间戳
    import_time = db.Column(db.DateTime, default=datetime.utcnow, comment='导入时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 订单状态常量
    STATUS_WAITING_ORDER = '等待下单'
    STATUS_ORDERED = '已下单'
    STATUS_PAID = '已支付'
    STATUS_SHIPPED = '已发货'
    STATUS_RECEIVED = '已收货'
    STATUS_ORDER_FAILED = '下单失败'
    STATUS_PAYMENT_FAILED = '付款失败'
    STATUS_CANCELLED = '已取消'
    
    def get_numeric_quantity(self, field_name='purchase_quantity'):
        """获取数值型数量，处理空值和非数值情况"""
        try:
            value = getattr(self, field_name)
            if value is None or value == '':
                return 0
            return float(value)
        except (ValueError, TypeError):
            return 0
    
    def get_numeric_price(self, field_name='purchase_price'):
        """获取数值型价格，处理空值和非数值情况"""
        try:
            value = getattr(self, field_name)
            if value is None or value == '':
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def calculate_total_amount(self):
        """计算订单总金额"""
        quantity = self.get_numeric_quantity()
        price = self.get_numeric_price()
        return quantity * price
    
    def is_pending_order(self):
        """判断是否为待下单状态"""
        return self.order_status == self.STATUS_WAITING_ORDER
    
    def is_completed(self):
        """判断订单是否已完成"""
        return self.order_status in [self.STATUS_RECEIVED]
    
    def is_failed(self):
        """判断订单是否失败"""
        return self.order_status in [self.STATUS_ORDER_FAILED, self.STATUS_PAYMENT_FAILED, self.STATUS_CANCELLED]
    
    def update_status(self, new_status, failure_reason=None, order_number=None, **kwargs):
        """更新订单状态"""
        self.order_status = new_status
        if failure_reason:
            self.failure_reason = failure_reason
        if order_number:
            self.order_number = order_number
        
        # 更新其他字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'store_id': self.store_id,
            'product_name': self.product_name,
            'sku_code': self.sku_code,
            'purchase_quantity': self.purchase_quantity,
            'purchase_price': self.purchase_price,
            'supplier': self.supplier,
            'received_quantity': self.received_quantity,
            'order_status': self.order_status,
            'order_number': self.order_number,
            'purchase_order_number': self.purchase_order_number,
            'logistics_number': self.logistics_number,
            'actual_payment': self.actual_payment,
            'failure_reason': self.failure_reason,
            'remarks': self.remarks,
            'from_user': self.from_user,
            'total_amount': self.calculate_total_amount(),
            'is_pending': self.is_pending_order(),
            'is_completed': self.is_completed(),
            'is_failed': self.is_failed(),
            'import_time': self.import_time.isoformat() if self.import_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number or self.id}({self.sku_code})>'