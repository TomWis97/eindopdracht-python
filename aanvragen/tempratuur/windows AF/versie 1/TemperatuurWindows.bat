@echo off

for /f "delims== tokens=2" %%a in (
    'wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature /value'
) do (
    set /a degrees_celsius=%%a / 10 - 273
)

echo %degrees_celsius%

pause
