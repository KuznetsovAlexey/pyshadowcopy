import wmi
import ctypes
import platform

class pyshadowcopy():
    """docstring"""

    def __init__(self,use_eventlog=True):
        """Constructor"""
        #Проверяем имеет ли права администратора. Win32_ShadowCopy требует прав администратора (или можно попытаться настроить рахрешения)
        self.is_admin()
        #Проверяем что Разрядность операционной системы соответствуют разрядности Python.
        # Не возможно вызвать из 32-битного Phyton запущеного на 64 битной - ОС ShadowCopy
        self. is_64bit()
        #Создаем объект для работы с wmi
        self.wmi = wmi.WMI()
        #Используем ли eventlog для фиксирования событий
        self.use_eventlog = use_eventlog

        #Множество со списком дисков
        self.system_disk = set()
        self.get_disk()

        # Множество со списком ID ShadowCopy
        self.shadowcopys_id = set()
        self.get_shadowcopys_id()

    def get_disk(self):
        #Функция получения списка доступных дисков
        self.system_disk = set()
        for disk in self.wmi.Win32_LogicalDisk(FileSystem = "NTFS"):
            self.system_disk.add(disk.Name)
        return self.system_disk

    def is_admin(self):
        #Проверяем наличие прав админисатртора
        if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            return True
        else:
            print("Attention!! No administrator rights. It will not work correctly!")
            return False

    def is_64bit(self):
        #проверяем запущен ли 64 битный python на 64 ОС, или 32 на 32.
        #В случае запуска 32 битного python на 64 битно ОС пишем предупреждение.
        if (platform.architecture()[0] == '64bit' and platform.machine() =='AMD64'):
            return True
        elif (platform.architecture()[0] == '32bit' and platform.machine() =='i386'):
            return True
        else:
            print("Attention!! The Python version does not match the architecture version (32 or 64). It will not work correctly!")
            return False

    def get_shadowcopys_id(self):
        #Получаем множество доступных ID снапшетов
        self.shadowcopys_id = set()
        for shadowcopy in self.wmi.Win32_ShadowCopy():
            self.shadowcopys_id.add(shadowcopy.ID)
        return self.shadowcopys_id

        #print(self.wmi.Win32_ShadowCopy[0])
        #or disk in self.wmi.Win32_ShadowCopy:
        #    print (disk)
