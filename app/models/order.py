"""
采购订单模型 - 支持订单状态跟踪和数据隔离
"""
from datetime import datetime
from app import db

class Order(db.Model):
    """采购订单模型"""
    __tablename__ = '收货单列表'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 基本订单信息
    store_id = db.Column(db.String(100))  # 门店ID
    product_name = db.Column(db.String(255))  # 商品名称
    sku_code = db.Column(db.String(255))  # SKU编码
    purchase_quantity = db.Column(db.String(50))  # 采购量
    purchase_price = db.Column(db.String(50))  # 采购单价
    supplier = db.Column(db.String(100))  # 供应商
    
    # 收货信息
    received_quantity = db.Column(db.String(50))  # 收货量
    remarks = db.Column(db.Text)  # 备注
    
    # 物流和订单信息
    logistics_number = db.Column(db.String(100))  # 物流单号
    order_number = db.Column(db.String(100))  # 订单编号
    order_status = db.Column(db.String(50))  # 订单状态
    failure_reason = db.Column(db.Text)  # 失败原因
    purchase_order_number = db.Column(db.String(100))  # 采购单号
    actual_payment = db.Column(db.String(50))  # 实际支付
    
    # 预留字段
    reserved_0 = db.Column(db.String(255))  # 预留0
    reserved_1 = db.Column(db.String(255))  # 预留1
    reserved_2 = db.Column(db.String(255))  # 预留2
    
    # 数据隔离字段
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 归属用户
    
    # 时间戳
    import_time = db.Column(db.DateTime, default=datetime.utcnow)  # 导入时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    owner = db.relationship('User', backref='orders')
    
    def can_access(self, user):
        """检查用户是否可以访问此订单"""
        if user.is_super():
            return True
        return self.from_user == user.id
    
    def get_status_display(self):
        """获取状态显示名称"""
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'shipped': '已发货',
            'delivered': '已送达',
            'completed': '已完成',
            'cancelled': '已取消',
            'failed': '失败'
        }
        return status_map.get(self.order_status, self.order_status)
    
    def is_completed(self):
        """检查订单是否已完成"""
        return self.order_status in ['completed', 'delivered']
    
    def is_active(self):
        """检查订单是否活跃"""
        return self.order_status not in ['completed', 'cancelled', 'failed']
    
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
            'remarks': self.remarks,
            'logistics_number': self.logistics_number,
            'order_number': self.order_number,
            'order_status': self.order_status,
            'status_display': self.get_status_display(),
            'failure_reason': self.failure_reason,
            'purchase_order_number': self.purchase_order_number,
            'actual_payment': self.actual_payment,
            'reserved_0': self.reserved_0,
            'reserved_1': self.reserved_1,
            'reserved_2': self.reserved_2,
            'from_user': self.from_user,
            'import_time': self.import_time.isoformat() if self.import_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'