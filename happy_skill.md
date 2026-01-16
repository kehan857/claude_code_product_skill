# Happy - Claude Code 移动控制工具

> Happy coder, happy life! 让你随时随地控制 Claude Code

## 简介

Happy 是一个强大的 Claude Code 移动控制工具，让你可以在移动端远程控制 Claude Code 会话，支持推送通知、后台服务管理等高级功能。

## 安装

```bash
npm install -g happy-coder
```

## 主要功能

### 1. 移动端控制 Claude Code
- 远程启动和管理 Claude Code 会话
- 支持多设备协同工作
- 实时推送通知

### 2. 多模式支持
- **Codex 模式**: 启动 Codex 编程模式
- **Gemini 模式 (ACP)**: 支持 Google Gemini API
- **标准模式**: 默认 Claude 模式

### 3. 推送通知
- 发送自定义推送消息
- 会话状态通知
- 任务完成提醒

### 4. 后台服务管理
- 远程启动后台服务
- 会话持久化
- 脱机工作支持

### 5. 系统诊断
- 健康检查
- 配置诊断
- 故障排查

## 命令参考

### 基础命令

```bash
# 启动 Claude 会话
happy

# 使用特定选项启动
happy --yolo                    # 跳过权限检查（谨慎使用）
happy --resume                  # 恢复最近的会话
happy --model opus              # 使用特定模型

# 认证管理
happy auth login                # 登录认证
happy auth login --force        # 强制重新登录
happy auth status               # 查看认证状态

# 启动不同模式
happy codex                     # Codex 模式
happy gemini                    # Gemini 模式

# 推送通知
happy notify "Hello World"      # 发送推送消息

# 后台服务管理
happy daemon start              # 启动后台服务
happy daemon stop               # 停止后台服务
happy daemon status             # 查看服务状态

# 系统诊断
happy doctor                    # 运行诊断

# API 密钥管理
happy connect                   # 连接 AI API 密钥
```

### 高级选项

Happy 支持所有 Claude Code 的命令行选项：

```bash
# 自定义 API 端点
happy --claude-env ANTHROPIC_BASE_URL=http://127.0.0.1:3456

# 添加工作目录
happy --add-dir /path/to/project

# 使用特定模型
happy --model sonnet
happy --model claude-opus-4-5-20251101

# 恢复特定会话
happy --resume <session-id>

# 调试模式
happy --debug

# 插件目录
happy --plugin-dir /path/to/plugins
```

## 使用场景

### 场景1: 移动端工作

```bash
# 在电脑上启动后台服务
happy daemon start

# 在移动端控制 Claude
happy notify "开始处理任务"
happy --resume
```

### 场景2: 推送通知

```bash
# 任务完成后发送通知
happy notify "代码重构已完成"

# 发送带emoji的消息
happy notify "✅ 部署成功！"
```

### 场景3: 远程诊断

```bash
# 检查系统健康状态
happy doctor

# 查看配置信息
happy --debug
```

### 场景4: 多模型切换

```bash
# 使用 Gemini 模式
happy gemini

# 使用 Codex 模式
happy codex

# 使用自定义 Claude 模型
happy --model opus
```

## 配置

Happy 的配置文件通常位于：
- macOS: `~/.config/happy/`
- Linux: `~/.config/happy/`
- Windows: `%APPDATA%\happy\`

### 环境变量

```bash
# API 密钥
export ANTHROPIC_API_KEY="your-api-key"

# 自定义 API 端点
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
```

## 故障排查

### 问题: 命令找不到

```bash
# 检查安装
npm list -g happy-coder

# 重新安装
npm uninstall -g happy-coder
npm install -g happy-coder
```

### 问题: 认证失败

```bash
# 强制重新登录
happy auth login --force
```

### 问题: 后台服务无法启动

```bash
# 运行诊断
happy doctor

# 查看服务状态
happy daemon status
```

## 技巧与最佳实践

1. **使用别名**: 为常用命令创建别名
   ```bash
   alias h='happy'
   alias hr='happy --resume'
   ```

2. **后台运行**: 结合 nohup 使用
   ```bash
   nohup happy daemon start &
   ```

3. **日志调试**: 使用调试模式排查问题
   ```bash
   happy --debug api,hooks
   ```

4. **会话管理**: 定期清理旧会话
   ```bash
   happy --resume | grep "old sessions"
   ```

## 相关资源

- [Happy NPM 包](https://www.npmjs.com/package/happy-coder)
- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [GitHub Issues](https://github.com/kehan857/claude_code_product_skill/issues)

## 更新日志

### v0.13.0 (当前版本)
- 支持 Claude Code v2.1.2
- 新增 Gemini 模式支持
- 改进推送通知功能
- 修复已知问题

## 许可证

MIT License

---

**维护者**: kehan857
**最后更新**: 2026-01-16
