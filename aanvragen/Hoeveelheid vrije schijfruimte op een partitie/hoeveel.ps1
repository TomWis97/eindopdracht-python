$disk = Get-WmiObject Win32_LogicalDisk |
Select-Object Size,FreeSpace,DeviceID

$disk.DeviceID
$disk.Size
$disk.FreeSpace

Pause