# Some examples below...

#ps | measure-object | select count | Out-File C:\scripts\log\agent_counters.txt
#ps | Export-Clixml c:\scripts\log\magweg.xml
#ps | Export-Csv C:\scripts\log\magweg.csv -Force -NoTypeInformation
#$a = ps | measure-object
#$a.Count
ps | measure-object | select -expandproperty count