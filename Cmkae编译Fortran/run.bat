@echo off
setlocal

@REM ======================== 设置变量 ========================
set "SOURCE_DIR=%~dp0"
set "BUILD_DIR=%SOURCE_DIR%build"
set "GENERATOR=Unix Makefiles"
set "LOG_FILE=build.log"

@REM ======================== 准备工作 ========================
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"
if exist "%LOG_FILE%" del "%LOG_FILE%"

@REM ======================== 编译项目 ========================
cd /d "%BUILD_DIR%"
cmake -G "%GENERATOR%" -S "%SOURCE_DIR%" >> "%LOG_FILE%"
cmake --build . >> "%LOG_FILE%"


@REM ======================== 运行可执行文件 ========================
set "EXECUTABLE_PATH=%BUILD_DIR%\src\main.exe"
if not exist "%EXECUTABLE_PATH%" (
    echo Error: Executable does not exist.
    exit /b 1
)
"%EXECUTABLE_PATH%"

endlocal