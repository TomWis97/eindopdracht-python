$m = Get-Service | Where-Object {$_.status -eq "running"} | measure-object
$m.Count