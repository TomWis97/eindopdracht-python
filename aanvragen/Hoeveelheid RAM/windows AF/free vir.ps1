﻿Get-WmiObject win32_OperatingSystem |%{"Free Virtual Memory : {0}KB" -f $_.freevirtualmemory}