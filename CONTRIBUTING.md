# 贡献指南 (Contributing Guide)

感谢您对智慧采购管理系统的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告错误
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 添加新功能

## 🤝 如何贡献

### 1. 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/your-username/intelligent-procurement-system/issues) 中是否已有相关问题
2. 如果没有，请创建新的 Issue
3. 使用清晰的标题和详细的描述
4. 如果是 bug 报告，请包含：
   - 操作系统和版本
   - Python 版本
   - 错误复现步骤
   - 错误信息和日志
   - 期望的行为

### 2. 提交代码

#### 准备工作

1. **Fork 仓库**
```bash
# 点击 GitHub 页面上的 Fork 按钮
# 然后克隆您的 fork
git clone https://github.com/your-username/intelligent-procurement-system.git
cd intelligent-procurement-system
```

2. **设置开发环境**
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest black flake8 isort
```

3. **添加上游仓库**
```bash
git remote add upstream https://github.com/original-owner/intelligent-procurement-system.git
```

#### 开发流程

1. **创建功能分支**
```bash
# 确保在最新的 main 分支
git checkout main
git pull upstream main

# 创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-fix-name
```

2. **进行开发**
   - 编写代码
   - 添加测试
   - 更新文档

3. **代码规范检查**
```bash
# 代码格式化
black .

# 导入排序
isort .

# 代码风格检查
flake8 .

# 运行测试
pytest
```

4. **提交更改**
```bash
git add .
git commit -m "feat: 添加新功能描述"
# 或
git commit -m "fix: 修复问题描述"
```

5. **推送分支**
```bash
git push origin feature/your-feature-name
```

6. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 填写 PR 模板
   - 等待代码审查

## 📝 代码规范

### Python 代码风格

我们遵循 PEP 8 标准，并使用以下工具：

- **Black**：代码格式化
- **isort**：导入语句排序
- **flake8**：代码风格检查

### 提交信息规范

使用语义化提交信息：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

**类型**：
- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更改
- `style`: 代码风格更改（不影响功能）
- `refactor`: 重构（既不修复问题也不添加功能）
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

**示例**：
```
feat(auth): 添加用户登录功能

- 实现用户名密码登录
- 添加会话管理
- 增加登录状态验证

Closes #123
```

### 代码注释

- 使用中文注释
- 为复杂逻辑添加详细说明
- 为公共 API 添加文档字符串

```python
def calculate_order_amount(quantity, price, discount=0):
    """
    计算订单总金额
    
    Args:
        quantity (int): 商品数量
        price (float): 单价
        discount (float): 折扣率，默认为0
        
    Returns:
        float: 订单总金额
        
    Raises:
        ValueError: 当数量或价格为负数时
    """
    if quantity < 0 or price < 0:
        raise ValueError("数量和价格不能为负数")
    
    total = quantity * price
    return total * (1 - discount)
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models.py

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

### 编写测试

为新功能编写测试：

```python
# tests/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.models.user import User

class TestUserService:
    def test_create_user(self):
        """测试用户创建"""
        user_data = {
            'username': 'testuser',
            'password': 'password123',
            'phone': '13800138000'
        }
        
        user = UserService.create_user(user_data)
        
        assert user.username == 'testuser'
        assert user.check_password('password123')
        assert user.phone == '13800138000'
```

## 📚 文档

### 更新文档

如果您的更改影响了用户界面或 API，请同时更新相关文档：

- `README.md` - 项目概述和快速开始
- `docs/deployment.md` - 部署指南
- `docs/usage.md` - 使用手册
- `docs/api.md` - API 文档

### 文档风格

- 使用清晰简洁的中文
- 提供代码示例
- 包含截图（如适用）
- 保持结构化的格式

## 🔍 代码审查

### 审查清单

提交 PR 前请检查：

- [ ] 代码遵循项目规范
- [ ] 添加了适当的测试
- [ ] 测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰
- [ ] 没有合并冲突

### 审查过程

1. 维护者会审查您的 PR
2. 可能会要求修改
3. 修改后重新审查
4. 通过后合并到主分支

## 🎯 开发优先级

当前开发重点：

1. **高优先级**
   - 性能优化
   - 安全增强
   - 关键 bug 修复

2. **中优先级**
   - 新功能开发
   - 用户体验改进
   - 文档完善

3. **低优先级**
   - 代码重构
   - 测试覆盖率提升
   - 工具链改进

## 📞 获取帮助

如果您在贡献过程中遇到问题：

1. 查看现有的 [Issues](https://github.com/your-username/intelligent-procurement-system/issues)
2. 在 [Discussions](https://github.com/your-username/intelligent-procurement-system/discussions) 中提问
3. 联系维护者：support@example.com

## 🏆 贡献者

感谢所有为项目做出贡献的开发者！

<!-- 这里会自动显示贡献者列表 -->

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下授权。

---

再次感谢您的贡献！每一个贡献都让这个项目变得更好。 🚀