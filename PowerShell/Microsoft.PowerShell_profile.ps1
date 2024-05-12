# -----------------------| 导包 |-----------------------
Import-Module PSReadLine
Import-Module posh-git
Import-Module Terminal-Icons

# -----------------------| 设置主题 |-----------------------
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/negligible.omp.json" | Invoke-Expression
$env:VIRTUAL_ENV_DISABLE_PROMPT=1

# -----------------------| 基本设置 |-----------------------
# 设置预测文本来源为历史记录
# Set-PSReadLineOption -PredictionSource History

# 每次回溯输入历史，光标定位于输入内容末尾
Set-PSReadLineOption -HistorySearchCursorMovesToEnd

# 设置 Tab 为菜单补全和 Intellisense
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete

# 设置向上键为后向搜索历史记录
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward

# 设置向下键为前向搜索历史纪录
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

# -----------------------| 链接 |-----------------------
Set-Alias -Name c -Value clear
Set-Alias -Name vim -Value nvim

# -----------------------| 函数 |-----------------------
function IntelOneapiVars {
    cmd.exe "/K" '"D:\Intel\oneAPI\setvars.bat" && pwsh --NoLogo' 
}

function ProxyGitSet {
    git config --global http.proxy http://127.0.0.1:20172
    git config --global https.proxy https://127.0.0.1:20172
    echo "git proxy has been setted."
}

function ProxyGitUnset {
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    echo "git proxy has been unsetted."
}

function ProxyScoopSet {
    scoop config proxy 127.0.0.1:20172
    echo "scoop proxy has been setted."
}

function ProxyScoopUnset {
    scoop config rm proxy
    echo "scoop proxy has been unsetted."
}
