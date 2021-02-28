# pyshadowcopy
A wrapper over the WMI Win32_ShadowCopy class for Python

#Устранение проблем с WMI классом ShadowCopy

sc config winmgmt start= disabled
net stop winmgmt
cd %windir%\system32\wbem
regsvr32 vsswmi.dll
wmiprvse /regserver
winmgmt /regserver
sc config winmgmt start= auto
net start winmgmt
mofcomp vss.mof

