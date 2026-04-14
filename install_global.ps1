# PhantomIP Global Installer
$currentPath = Get-Location
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($userPath -like "*$currentPath*") {
    Write-Host "[!] PhantomIP is already in your PATH." -ForegroundColor Yellow
} else {
    Write-Host "[!] Adding $currentPath to User PATH..." -ForegroundColor Green
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$currentPath", "User")
    Write-Host "[+] Installation Complete. RESTART your terminal to use 'PhantomIP' from anywhere!" -ForegroundColor Green
}
