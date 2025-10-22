"""
门店模型
定义门店相关的数据结构和操作
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Store(db.Model):
    """门店模型"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100), unique=True, nullable=False, comment='门店ID/仓库编码')
    store_name = db.Column(db.String(100), nullable=False, comment='门店名称')
    
    # 地址信息
    address = db.Column(db.String(255), comment='详细地址')
    province = db.Column(db.String(50), comment='省份')
    city = db.Column(db.String(50), comment='城市')
    district = db.Column(db.String(50), comment='区县')
    postcode = db.Column(db.String(20), comment='邮编')
    district_code = db.Column(db.String(20), comment='地址编码')
    
    # 联系信息
    phone = db.Column(db.String(20), comment='电话')
    mobile = db.Column(db.String(20), comment='手机')
    contact_name = db.Column(db.String(50), comment='联系人')
    
    # 阿里巴巴API凭证
    alibaba_openid = db.Column(db.String(100), comment='阿里巴巴OpenID')
    alibaba_openkey = db.Column(db.String(100), comment='阿里巴巴OpenKey')
    alibaba_token = db.Column(db.String(100), comment='阿里巴巴Token')
    
    # 归属和权限
    from_user = db.Column(db.String(100), nullable=False, comment='归属用户')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def get_full_address(self):
        """获取完整地址"""
        parts = [self.province, self.city, self.district, self.address]
        return ''.join(filter(None, parts))
    
    def has_alibaba_config(self):
        """检查是否配置了阿里巴巴API"""
        return all([self.alibaba_openid, self.alibaba_openkey, self.alibaba_token])
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'store_id': self.store_id,
            'store_name': self.store_name,
            'address': self.address,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'postcode': self.postcode,
            'phone': self.phone,
            'mobile': self.mobile,
            'contact_name': self.contact_name,
            'from_user': self.from_user,
            'has_alibaba_config': self.has_alibaba_config(),
            'full_address': self.get_full_address(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Store {self.store_name}({self.store_id})>'