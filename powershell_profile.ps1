# Setup:
# Make hardlink with mklink /h prof .\powershell_profile.ps1
# copy hardlink to ~\Documents\WindowsPowerShell\_Microsoft.PowerShell_profile.ps1
# Backup old file!
# default encoding was UCS-2 LE BOM (UTF16 LE) whyever, utf8 seems to work

# Vim on windows

$VIMPATH    = "C:\Program Files (x86)\Vim\vim82\vim.exe"

Set-Alias vi   $VIMPATH
Set-Alias vim  $VIMPATH

# for editing your PowerShell profile
Function Edit-Profile
{
    vim $profile
}

# for editing your Vim settings
Function Edit-Vimrc
{
    vim $home\_vimrc
}

Function wex
{
    if ($args[0] -eq $null){
        explorer.exe .
    } else {
        explorer.exe $args[0]
    }
}


# make wt callable with the current working directory
# or in home if started from startbar
$__path1=pwd
$__path2="C:\WINDOWS\system32"
if ((Join-Path $__path1 '') -eq (Join-Path $__path2 '')){
    cd ~  # cd to home directory if started in sys32
}

# start python in wt, not in new cmd
$env:pathext = $env:pathext + ";.PY"

# git encoding
$env:LC_ALL='C.UTF-8'


#Aliasses
Set-Alias ll ls
