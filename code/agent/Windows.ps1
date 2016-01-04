function temperature
{
    $a = get-wmiobject MSAcpi_ThermalZoneTemperature -namespace "root/wmi" `
        | select CurrentTemperature,InstanceName | Select-Object -First 1
    ($a.CurrentTemperature/10 - 273.15) * 1.8 + 32
}

function ram_total
{
    Get-WmiObject win32_OperatingSystem |%{"{0}" -f $_.totalvisiblememorysize / 1024}
}

function ram_free
{
    Get-WmiObject win32_OperatingSystem |%{"{0}" -f $_.freephysicalmemory / 1024}
}

function no_services
{
    $services = Get-Service | Where-Object {$_.status -eq "running"} | Measure
    $services.count
}

function diskinfo
{
    Get-WmiObject Win32_LogicalDisk | Select-Object Size,FreeSpace,DeviceID | Where-Object {$_.Size -ne $null} | ForEach-Object { Write-Host $_.DeviceID $_.Size $_.FreeSpace }
}

function no_users
{
    $users = Get-WMIObject Win32_Process -filter 'name="explorer.exe"' |
     ForEach-Object { $owner = $_.GetOwner(); '{0}\{1}' -f $owner.Domain, $owner.User } |
     Sort-Object | Get-Unique | Measure
    $users.count
}

function ips
{
    $ips = Get-NetIPAddress
    $ips | ForEach-Object {Write-Host $_.IPAddress $_.PrefixLength}
}

function uptime
{
    $lastboottime = (Get-WmiObject -Class Win32_OperatingSystem).LastBootUpTime
    $sysuptime = (Get-Date) – [System.Management.ManagementDateTimeconverter]::ToDateTime($lastboottime) 
    $sysuptime.TotalMinutes
}

function cpu_load
{
    $proc =get-counter -Counter "\Processor(_Total)\% Processor Time" -SampleInterval 2
    $cpu=($proc.readings -split ":")[-1]
    $cpu
}

function no_processes
{
    $processes = Get-Service | Where-Object {$_.status -eq "running"} | measure
    $processes.Count
}