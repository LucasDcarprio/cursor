"""
商品模型
定义商品基础数据的结构和操作
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    """商品基础数据模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 商品基本信息
    barcode = db.Column(db.Text, comment='商品条码（支持多个）')
    sku_code = db.Column(db.Text, comment='SKU编码（支持多个）')
    product_name = db.Column(db.String(255), comment='门店商品名称')
    specification = db.Column(db.String(255), comment='门店规格')
    
    # 采购相关信息
    purchase_attributes = db.Column(db.String(255), comment='采购商品属性')
    settlement_link = db.Column(db.String(255), comment='结算链接')
    units_per_package = db.Column(db.String(255), comment='每份单件数')
    min_purchase_qty = db.Column(db.String(255), comment='起购数')
    retail_price = db.Column(db.String(255), comment='美团售价')
    manufacturer = db.Column(db.String(255), comment='厂家')
    
    # 物流和费用
    has_shipping_fee = db.Column(db.String(255), comment='是否有运费')
    historical_cost = db.Column(db.String(255), comment='历史进价')
    
    # 平台相关
    product_id = db.Column(db.String(255), comment='商品ID')
    spec_id = db.Column(db.String(255), comment='规格ID')
    platform_attributes = db.Column(db.String(255), comment='平台属性列表')
    order_mode = db.Column(db.String(255), comment='下单模式')
    purchase_channel = db.Column(db.String(255), comment='采购渠道')
    
    # 备注和预留字段
    remarks = db.Column(db.String(255), comment='备注')
    reserved_0 = db.Column(db.String(255), comment='预留字段0')
    reserved_1 = db.Column(db.String(255), comment='预留字段1')
    reserved_2 = db.Column(db.String(255), comment='预留字段2')
    
    # 归属和权限
    from_user = db.Column(db.String(100), nullable=False, comment='归属用户')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def get_sku_codes_list(self):
        """获取SKU编码列表"""
        if not self.sku_code:
            return []
        return [code.strip() for code in self.sku_code.split(',') if code.strip()]
    
    def get_barcodes_list(self):
        """获取条码列表"""
        if not self.barcode:
            return []
        return [code.strip() for code in self.barcode.split(',') if code.strip()]
    
    def is_alibaba_product(self):
        """判断是否为阿里巴巴商品"""
        return self.purchase_channel and '阿里巴巴' in self.purchase_channel
    
    def get_numeric_value(self, field_name, default=0):
        """获取数值字段的值，处理空值和非数值情况"""
        try:
            value = getattr(self, field_name)
            if value is None or value == '':
                return default
            return float(value)
        except (ValueError, TypeError):
            return default
    
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
            'units_per_package': self.units_per_package,
            'min_purchase_qty': self.min_purchase_qty,
            'retail_price': self.retail_price,
            'manufacturer': self.manufacturer,
            'has_shipping_fee': self.has_shipping_fee,
            'historical_cost': self.historical_cost,
            'product_id': self.product_id,
            'spec_id': self.spec_id,
            'platform_attributes': self.platform_attributes,
            'order_mode': self.order_mode,
            'purchase_channel': self.purchase_channel,
            'remarks': self.remarks,
            'from_user': self.from_user,
            'is_alibaba_product': self.is_alibaba_product(),
            'sku_codes_list': self.get_sku_codes_list(),
            'barcodes_list': self.get_barcodes_list(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.product_name}({self.sku_code})>'