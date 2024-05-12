@echo off
setlocal enabledelayedexpansion

:: 设置源文件和目标文件的路径
set "source=F:\Project\CodeTemplate\PowerShell\Microsoft.PowerShell_profile.ps1"
set "destination=C:\Users\Virgo\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"

:: 检查目标文件是否存在
if exist "%destination%" (
    set /p "response=文件已存在，是否覆盖？(Y/N) [Y] "
    :: 如果用户没有输入，将response设置为"Y"
    if not defined response (
        set "response=Y"
    )
    :: 根据用户输入决定是否覆盖
    if /i "!response!"=="Y" (
        echo 覆盖文件...
        copy /y "%source%" "%destination%"
    ) else (
        echo 操作已取消。
        goto end
    )
) else (
    echo 复制文件...
    copy /y "%source%" "%destination%"
)

:end
echo 操作完成。
pause
endlocal