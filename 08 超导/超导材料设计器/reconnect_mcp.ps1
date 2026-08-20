$ErrorActionPreference = "SilentlyContinue"
$RepoSrc = "D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_ai_repo\src"
$HttpPort = 8000
$WsPort = 9500

Write-Host "=== MCP重连助手 ===" -ForegroundColor Cyan

$pyRunning = Get-Process | Where-Object { $_.ProcessName -eq "python" }
if (-not $pyRunning) {
	Write-Host "Python服务器未运行, 正在重启..." -ForegroundColor Yellow
	$env:PYTHONPATH = $RepoSrc
	Start-Process -FilePath "python" `
		-ArgumentList @("-u", "-m", "godot_ai", "--transport", "streamable-http", "--port", $HttpPort, "--ws-port", $WsPort) `
		-WindowStyle Minimized
	for ($i = 0; $i -lt 15; $i++) {
		Start-Sleep -Seconds 2
		$ports = netstat -an | Select-String ":$HttpPort\s+.*LISTENING"
		if ($ports) { Write-Host "服务器已就绪" -ForegroundColor Green; break }
	}
} else {
	Write-Host "Python服务器正在运行 (PID: $($pyRunning.Id))" -ForegroundColor Green
}

$godotRunning = Get-Process | Where-Object { $_.ProcessName -like "*Godot*" }
if (-not $godotRunning) {
	Write-Host "Godot编辑器未运行, 正在启动..." -ForegroundColor Yellow
	Start-Process -FilePath "F:\Program Files\Godot\Godot_v4.6.2-stable_win64.exe" `
		-ArgumentList @("--editor", "--path", "`"D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_project`"")
	Start-Sleep -Seconds 5
}

Write-Host "请在CodeArts中重新调用MCP工具 (会自动重连)" -ForegroundColor Cyan