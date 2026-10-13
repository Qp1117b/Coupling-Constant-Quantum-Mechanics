@echo off
chcp 65001 >nul
title CQM 研究站服务（Spring Boot）
cd /d "%~dp0"

echo ============================================================
echo   CQM 研究站服务（Spring Boot 3.3 / JDK 21+）
echo.
echo   入口:  http://127.0.0.1:8080/            （理论阅读站 · VitePress）
echo   API :  http://127.0.0.1:8080/api/status  （状态读数）
echo          http://127.0.0.1:8080/api/sparql?query=...
echo          http://127.0.0.1:8080/api/search?q=...
echo          http://127.0.0.1:8080/api/review  （证据复核）
echo.
echo   依赖从阿里云镜像拉取（本机直连 Maven 中央仓库不通）。
echo   首次启动会下载依赖，请耐心等待；关闭本窗口即停止服务。
echo.
echo   注：本目录含中文与空格，mvn spring-boot:run 在 fork JVM 时
echo       会报 ClassNotFoundException，故一律用 package + java -jar。
echo ============================================================
echo.

if "%JAVA_HOME%"=="" (
  echo [提示] 未设置 JAVA_HOME，使用 PATH 中的 java。
)

if not exist "target\cqm-station-1.0.0.jar" (
  echo [1/2] 未找到可执行 jar，先打包...
  mvn -s "%~dp0settings.xml" package -DskipTests
  if errorlevel 1 (
    echo [失败] 打包未成功，详见上方输出。
    pause
    exit /b 1
  )
) else (
  echo [1/2] 已存在 target\cqm-station-1.0.0.jar，跳过打包
  echo       （改过代码或配置后，请先手工执行 mvn -s settings.xml package -DskipTests）
)

echo [2/2] 启动服务...（就绪后自动在浏览器打开研究站）
rem 延迟打开浏览器：等 Tomcat 就绪（独立进程，不阻塞服务）
start "" /min cmd /c "timeout /t 12 /nobreak >nul & start "" http://127.0.0.1:8080/"
java -jar "target\cqm-station-1.0.0.jar" --server.port=8080

echo.
echo 服务已停止。
pause
