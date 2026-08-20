param(
	[switch]$NoEditor,
	[switch]$Reload
)

$ErrorActionPreference = "SilentlyContinue"
$RepoSrc = "D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_ai_repo\src"
$GodotExe = "F:\Program Files\Godot\Godot_v4.6.2-stable_win64.exe"
$ProjectPath = "D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_project"
$HttpPort = 8000
$WsPort = 9500

Write-Host "=== CQM 超导材料设计器 - MCP环境一键启动 ===" -ForegroundColor Cyan

# 1. 清理旧进程
$oldPy = Get-Process | Where-Object { $_.ProcessName -eq "python" -and $_.StartTime -lt (Get-Date).AddSeconds(-2) }
if ($oldPy) { $oldPy | Stop-Process -Force; Write-Host "已清理旧Python进程" -ForegroundColor Yellow }
$oldGodot = Get-Process | Where-Object { $_.ProcessName -like "*Godot*" }
if ($oldGodot -and -not $NoEditor) { $oldGodot | Stop-Process -Force; Write-Host "已清理旧Godot进程" -ForegroundColor Yellow }
Start-Sleep -Seconds 2

# 2. 启动Python MCP服务器 (外部, 不被编辑器管理)
$env:PYTHONPATH = $RepoSrc
$reloadArg = if ($Reload) { @("--reload") } else { @() }
Start-Process -FilePath "python" `
	-ArgumentList @("-u", "-m", "godot_ai", "--transport", "streamable-http", "--port", $HttpPort, "--ws-port", $WsPort) + $reloadArg `
	-WindowStyle Minimized
Write-Host "Python MCP服务器启动中 (端口 $HttpPort, WebSocket $WsPort)..." -ForegroundColor Green

# 3. 等待服务器就绪
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
	Start-Sleep -Seconds 2
	$ports = netstat -an | Select-String ":$HttpPort\s+.*LISTENING"
	if ($ports) {
		$ready = $true
		Write-Host "MCP服务器就绪 (等待 $($i*2)秒)" -ForegroundColor Green
		break
	}
}
if (-not $ready) {
	Write-Host "警告: MCP服务器未在60秒内就绪" -ForegroundColor Red
	Write-Host "可能原因: 依赖缺失, 请运行 pip install pydantic fastmcp mcp" -ForegroundColor Yellow
}

# 4. 启动Godot编辑器 (带GUI)
if (-not $NoEditor) {
	Start-Process -FilePath $GodotExe -ArgumentList @("--editor", "--path", "`"$ProjectPath`"")
	Write-Host "Godot编辑器启动中 (带GUI)..." -ForegroundColor Green
	Start-Sleep -Seconds 5
	Write-Host "编辑器将自动adopt端口 $HttpPort 上的外部服务器" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== 启动完成 ===" -ForegroundColor Cyan
Write-Host "规则:" -ForegroundColor Yellow
Write-Host "  1. 不要调用 editor_reload_plugin (会断联)" -ForegroundColor White
Write-Host "  2. 不要用headless模式启动编辑器" -ForegroundColor White
Write-Host "  3. 服务器独立运行, 编辑器重启不影响" -ForegroundColor White
Write-Host "  4. 如需重连: 关闭编辑器重开即可 (服务器不动)" -ForegroundColor White
Write-Host ""
Write-Host "停止服务器: Stop-Process -Name python -Force" -ForegroundColor Gray