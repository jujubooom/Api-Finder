# 贡献指南 (Contributing Guide)

感谢您对 Api-Finder 项目的关注！我们欢迎所有形式的贡献。

## 如何贡献 (How to Contribute)

### 报告问题 (Reporting Issues)

如果您发现了问题或有功能建议，请：

1. 在提交Issue之前，请先搜索是否已有类似问题
2. 使用清晰的标题描述问题
3. 提供详细的复现步骤
4. 包含环境信息（操作系统、Python版本等）
5. 如果是功能建议，请说明使用场景

### 提交代码 (Submitting Code)

#### 开发环境设置

1. **Fork 项目**
   ```bash
   git clone https://github.com/jujubooom/Api-Finder.git
   cd api-finder
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

#### 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加新的输出格式支持
fix: 修复代理连接超时问题
docs: 更新README安装说明
```

#### Pull Request 流程

1. 创建功能分支
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 提交更改
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   ```

3. 推送到您的Fork
   ```bash
   git push origin feature/your-feature-name
   ```

4. 创建Pull Request

### 代码审查 (Code Review)

所有代码更改都需要通过代码审查：

- 确保代码符合项目规范
- 添加适当的测试
- 更新相关文档
- 确保所有测试通过

## 开发指南 (Development Guidelines)

### 项目结构

```
Api-Finder/
├── apifinder/          # 核心代码
├── config/             # 配置文件
├── docs/               # 文档
├── tests/              # 测试文件
├── main.py             # 入口文件
└── requirements.txt    # 依赖文件
```

### 文档

- 更新相关文档
- 添加代码注释
- 更新README（如需要）

## 许可证 (License)

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

## 联系方式 (Contact)

如果您有任何问题，请：

- 在GitHub上创建Issue
- 邮箱联系

感谢您的贡献！🎉 