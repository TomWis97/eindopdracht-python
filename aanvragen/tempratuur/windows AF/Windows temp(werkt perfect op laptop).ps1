$a = get-wmiobject MSAcpi_ThermalZoneTemperature -namespace "root/wmi" `
    | select CurrentTemperature,InstanceName
($a.CurrentTemperature/10 - 273.15) * 1.8 + 32