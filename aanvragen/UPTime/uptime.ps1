$lastboottime = (Get-WmiObject -Class Win32_OperatingSystem).LastBootUpTime

$sysuptime = (Get-Date) – [System.Management.ManagementDateTimeconverter]::ToDateTime($lastboottime) 
  
Write-Host "De computer staat aan voor: " $sysuptime.days "dagen" $sysuptime.hours "uur" $sysuptime.minutes "minuten" $sysuptime.seconds "seconden"