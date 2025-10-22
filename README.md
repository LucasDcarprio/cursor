# 智慧采购管理系统 (Intelligent Procurement Management System)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

一个面向零售连锁企业、商超等多门店经营实体的 SaaS 采购管理平台，与阿里巴巴 1688 平台深度集成，提供全流程的采购管理解决方案。

## 🚀 项目特色

- **多租户架构**：支持多企业、多门店独立使用
- **深度集成**：与阿里巴巴 1688 平台 API 深度对接，支持外部 API 访问
- **全流程管理**：从采购需求到收货确认的完整闭环
- **移动友好**：响应式设计，支持移动端操作
- **数据驱动**：提供采购数据分析和决策支持
- **权限控制**：基于角色的多级权限管理
- **自动化采购**：支持批量下单和自动支付

## 📋 功能模块

### 🔐 用户管理
- 用户注册、登录、权限管理
- 多角色支持（超级管理员、管理员、普通用户）
- 支持邮箱或手机注册
- 用户租用信息管理（门店数量、到期时间）

### 🏪 门店管理
- 门店信息维护和权限分配
- 多门店数据隔离
- 门店配送地址管理
- 阿里巴巴 API 凭证配置

### 📦 基础数据管理
- 商品基础信息管理
- SKU 编码管理
- 供应商信息维护
- 价格历史记录
- 支持 Excel 批量导入导出

### 🛒 采购订单管理
- 采购需求录入
- 订单状态跟踪
- 批量下单处理
- 收货确认管理
- 自动化支付流程

### 🔗 阿里巴巴集成
- 商品信息查询
- 自动下单和支付
- 物流信息同步
- 优惠券自动领取
- 订单状态实时更新

### 📊 数据管理
- Excel 数据导入导出
- 数据统计分析
- 操作日志记录
- 报表生成

## 🛠️ 技术栈

### 后端技术
- **Web 框架**：Flask 2.3+
- **数据库 ORM**：SQLAlchemy
- **身份认证**：Flask-Login
- **数据处理**：Pandas、NumPy
- **API 请求**：Requests
- **文件处理**：openpyxl、xlsxwriter
- **日志管理**：Python logging

### 前端技术
- **UI 框架**：Element Plus + Vue 3
- **CSS 框架**：Bootstrap 5
- **图标库**：Font Awesome
- **图表库**：ECharts
- **HTTP 客户端**：Axios

### 数据库
- **主数据库**：SQLite 3（开发环境）
- **生产数据库**：支持 MySQL、PostgreSQL

## 📁 项目结构

```
intelligent-procurement-system/
├── app/                          # 主应用目录
│   ├── __init__.py              # 应用初始化
│   ├── models/                  # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   ├── store.py            # 门店模型
│   │   ├── product.py          # 商品模型
│   │   └── order.py            # 订单模型
│   ├── views/                   # 视图层
│   │   ├── __init__.py
│   │   ├── auth.py             # 认证视图
│   │   ├── admin.py            # 管理视图
│   │   ├── api.py              # API 视图
│   │   └── alibaba.py          # 阿里巴巴集成
│   ├── services/                # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py     # 用户服务
│   │   ├── order_service.py    # 订单服务
│   │   └── alibaba_service.py  # 阿里巴巴服务
│   ├── utils/                   # 工具函数
│   │   ├── __init__.py
│   │   ├── decorators.py       # 装饰器
│   │   ├── helpers.py          # 辅助函数
│   │   └── validators.py       # 验证器
│   ├── static/                  # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/               # 模板文件
├── migrations/                   # 数据库迁移
├── tests/                       # 测试文件
├── docs/                        # 文档
├── alibaba_api.py              # 阿里巴巴 API 集成
├── mail.py                     # 邮件服务
├── config.py                   # 配置文件
├── requirements.txt            # Python 依赖
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- SQLite 3
- 阿里巴巴 1688 开放平台 API 凭证

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/intelligent-procurement-system.git
cd intelligent-procurement-system
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境**
```bash
cp config.py.example config.py
# 编辑 config.py 文件，填入您的配置信息
```

5. **初始化数据库**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **运行应用**
```bash
python main.py
```

访问 `http://localhost:5000` 即可使用系统。

### 配置说明

在 `config.py` 文件中配置以下信息：

```python
# 阿里巴巴 API 配置
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"  
API_TOKEN = "your_api_token"

# 数据库配置
DATABASE_URL = "sqlite:///app.db"

# 邮件配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USERNAME = "your_email@qq.com"
MAIL_PASSWORD = "your_mail_password"
```

## 📖 使用说明

### 1. 用户注册和登录
- 访问系统首页进行用户注册
- 填写企业信息和门店信息
- 登录后进入管理后台

### 2. 门店管理
- 在门店管理页面添加和配置门店信息
- 配置阿里巴巴 API 凭证
- 设置收货地址信息

### 3. 基础数据管理
- 导入商品基础数据（支持 Excel 格式）
- 维护 SKU 编码和商品信息
- 设置供应商和价格信息

### 4. 采购流程
- 创建采购需求
- 系统自动匹配商品信息
- 批量下单到阿里巴巴平台
- 自动支付和物流跟踪

### 5. 数据分析
- 查看采购统计报表
- 分析供应商表现
- 导出数据进行进一步分析

## 🔧 API 文档

系统提供完整的 RESTful API 接口，支持外部系统集成。

### 认证
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### 获取订单列表
```http
GET /api/orders?page=1&size=20&status=pending
Authorization: Bearer {token}
```

更多 API 文档请参考 [API 文档](docs/api.md)。

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 开发规范

- **Python**：遵循 PEP 8 规范
- **JavaScript**：使用 ESLint 和 Prettier
- **提交信息**：使用语义化提交信息
- **测试**：新功能需要添加相应测试

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢阿里巴巴开放平台提供的 API 支持
- 感谢所有开源项目的贡献者
- 感谢测试用户提供的宝贵反馈

## 📞 联系我们

- **项目维护者**：泓枢智创团队
- **邮箱**：support@example.com
- **官网**：https://example.com

## 🔗 相关链接

- [阿里巴巴开放平台](https://open.1688.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Element Plus 文档](https://element-plus.org/)

---

⭐ 如果这个项目对您有帮助，请给我们一个 Star！