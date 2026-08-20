@echo off
set PYTHONPATH=D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_ai_repo\src
start "MCP Server" /min python -u -m godot_ai --transport streamable-http --port 8000 --ws-port 9500
timeout /t 15 /nobreak >nul
start "Godot Editor" "F:\Program Files\Godot\Godot_v4.6.2-stable_win64.exe" --editor --path "D:\WorkSpace\物理\CQMFormal\08 超导\超导材料设计器\godot_project"