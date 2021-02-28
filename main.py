import pyshadowcopy
import ctypes
import os

print("Создаем объект")
sc= pyshadowcopy.pyshadowcopy()

print("Делаем телевую копию")
print(sc.create_shadowcopy_by_drive("c:"))

print("Получаем списоккопий")
print(sc.get_shadowcopys_id())

print("Получаем инфу")
print(sc.get_information_shadowcopy_by_id("D5DEAEEC-351A-4288-B69B-58F57A1299C7"))

print("монтирует")
print(sc.mount_shadowcopy_by_id("D5DEAEEC-351A-4288-B69B-58F57A1299C7", "C:\\temp\\test"))

print("отмонтируем")
print(sc.unmount_current_shadowcopy())

print("Удяляем все")
#print(sc.delete_all_shadowcopys())



#id="{38D5092A-A46B-44CE-BB7E-10AF642DD05A}"
#wmi=wmi.WMI()
#print(wmi.Win32_ShadowCopy(ID="{38D5092A-A46B-44CE-BB7E-10AF642DD05A}"))

#for shadowcopy in wmi.Win32_ShadowCopy(ID=id):
#    print(shadowcopy.Delete_())

#print ("\\\\?\\D:\\temp")
#mklink = ctypes.windll.LoadLibrary("kernel32.dll")
#print(mklink.CreateSymbolicLinkW("\\\\?\\c:\\temp\\01.dbf", "\\\\?\\c:\\temp\\0001.dbf", 0))

#os.unlink("\\\\?\\C:\\temp\\test")