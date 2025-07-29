"""
门店模型 - 支持多门店管理和数据隔离
"""
from datetime import datetime
from app import db

class Store(db.Model):
    """门店模型"""
    __tablename__ = 'store'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100), unique=True, nullable=False)  # 门店ID/仓库编码
    store_name = db.Column(db.String(100), nullable=False)  # 门店名称
    address = db.Column(db.String(255))  # 地址
    phone = db.Column(db.String(20))  # 电话
    mobile = db.Column(db.String(20))  # 手机
    contact_name = db.Column(db.String(50))  # 联系人
    province = db.Column(db.String(50))  # 省份
    city = db.Column(db.String(50))  # 城市
    district = db.Column(db.String(50))  # 区
    postcode = db.Column(db.String(20))  # 邮编
    district_code = db.Column(db.String(20))  # 地址编码
    
    # 阿里巴巴API凭证(门店级别)
    alibaba_openid = db.Column(db.String(100))
    alibaba_openkey = db.Column(db.String(100))
    alibaba_token = db.Column(db.String(100))
    
    # 数据隔离字段
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 归属用户
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    owner = db.relationship('User', backref='stores')
    
    def has_alibaba_credentials(self):
        """检查是否配置了阿里巴巴凭证"""
        return all([self.alibaba_openid, self.alibaba_openkey, self.alibaba_token])
    
    def can_access(self, user):
        """检查用户是否可以访问此门店"""
        if user.is_super():
            return True
        return self.from_user == user.id
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'store_id': self.store_id,
            'store_name': self.store_name,
            'address': self.address,
            'phone': self.phone,
            'mobile': self.mobile,
            'contact_name': self.contact_name,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'postcode': self.postcode,
            'district_code': self.district_code,
            'has_alibaba_credentials': self.has_alibaba_credentials(),
            'from_user': self.from_user,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Store {self.store_name}>'