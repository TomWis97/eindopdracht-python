﻿Get-WmiObject win32_OperatingSystem |%{"Free Physical Memory : {0}KB" -f $_.freephysicalmemory}