"""
商品基础数据模型 - 支持SKU管理和数据隔离
"""
from datetime import datetime
from app import db

class Product(db.Model):
    """商品基础数据模型"""
    __tablename__ = 'data'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 商品基本信息
    barcode = db.Column(db.Text)  # 商品条码(可支持多个)
    sku_code = db.Column(db.Text)  # SKU编码(可支持多个)
    product_name = db.Column(db.String(255))  # 门店商品名称
    specification = db.Column(db.String(255))  # 门店规格
    
    # 采购相关信息
    purchase_attributes = db.Column(db.String(255))  # 采购商品属性
    settlement_link = db.Column(db.String(255))  # 结算链接
    unit_count = db.Column(db.String(255))  # 每份单件数
    min_order = db.Column(db.String(255))  # 起购数
    meituan_price = db.Column(db.String(255))  # 美团售价
    manufacturer = db.Column(db.String(255))  # 厂家
    
    # 预留字段
    reserved_0 = db.Column(db.String(255))  # 预留0
    has_shipping = db.Column(db.String(255))  # 是否有运费
    price_history = db.Column(db.String(255))  # 历史进价
    
    # 平台相关信息
    goods_id = db.Column(db.String(255))  # 商品ID
    spec_id = db.Column(db.String(255))  # 规格ID
    platform_attributes = db.Column(db.String(255))  # 平台属性列表
    order_mode = db.Column(db.String(255))  # 下单模式
    purchase_channel = db.Column(db.String(255))  # 采购渠道
    
    # 其他信息
    remarks = db.Column(db.String(255))  # 备注
    reserved_1 = db.Column(db.String(255))  # 预留1
    reserved_2 = db.Column(db.String(255))  # 预留2
    
    # 数据隔离字段
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 归属用户
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    owner = db.relationship('User', backref='products')
    
    def can_access(self, user):
        """检查用户是否可以访问此商品"""
        if user.is_super():
            return True
        return self.from_user == user.id
    
    def get_sku_list(self):
        """获取SKU编码列表"""
        if not self.sku_code:
            return []
        return [sku.strip() for sku in self.sku_code.split(',') if sku.strip()]
    
    def get_barcode_list(self):
        """获取条码列表"""
        if not self.barcode:
            return []
        return [code.strip() for code in self.barcode.split(',') if code.strip()]
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'barcode': self.barcode,
            'sku_code': self.sku_code,
            'product_name': self.product_name,
            'specification': self.specification,
            'purchase_attributes': self.purchase_attributes,
            'settlement_link': self.settlement_link,
            'unit_count': self.unit_count,
            'min_order': self.min_order,
            'meituan_price': self.meituan_price,
            'manufacturer': self.manufacturer,
            'reserved_0': self.reserved_0,
            'has_shipping': self.has_shipping,
            'price_history': self.price_history,
            'goods_id': self.goods_id,
            'spec_id': self.spec_id,
            'platform_attributes': self.platform_attributes,
            'order_mode': self.order_mode,
            'purchase_channel': self.purchase_channel,
            'remarks': self.remarks,
            'reserved_1': self.reserved_1,
            'reserved_2': self.reserved_2,
            'from_user': self.from_user,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Product {self.product_name}>'