Get-Service | Where-Object {$_.status -eq "running"}
pause