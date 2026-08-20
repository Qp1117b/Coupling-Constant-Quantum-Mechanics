# CQM 超导材料设计器 - AI代理规则

## MCP连接规则 (强制)

1. **禁止调用 `editor_reload_plugin`** — 会销毁WebSocket并使MCP会话过期
2. **Godot必须带GUI启动** — headless模式不启动MCP服务器
3. **服务器独立运行** — 用 `start_mcp.ps1` 启动, 编辑器重启不影响服务器
4. **断联恢复** — 用 `reconnect_mcp.ps1` 或在编辑器godot-ai面板重连

## 启动

```powershell
# 一键启动 (服务器 + 编辑器)
.\start_mcp.ps1

# 仅启动服务器 (编辑器已开)
.\start_mcp.ps1 -NoEditor

# 带热重载 (改Python代码自动重启)
.\start_mcp.ps1 -Reload

# 断联重连
.\reconnect_mcp.ps1
```

## 验证

```powershell
# Headless验证脚本编译 (不启动MCP)
& "F:\Program Files\Godot\Godot_v4.6.2-stable_win64.exe" --headless --editor --quit --path "D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_project"
```