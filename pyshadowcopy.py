import wmi
import ctypes

class pyshadowcopy():
    """docstring"""

    def __init__(self,use_eventlog=True):
        """Constructor"""
        #Проверяем имеет ли права администратора. Win32_ShadowCopy требует прав администратора (или можно попытаться настроить рахрешения)
        self.is_admin()
        #Создаем объект для работы с wmi
        self.wmi = wmi.WMI()
        #Используем ли eventlog для фиксирования событий
        self.use_eventlog = use_eventlog

        #Множество со списком дисков
        self.system_disk = set()
        self.get_disk()

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

    def get_shadowcopy_id(self):
        #Получаем множество доступных ID снапшетов
        c = wmi.WMI()
        wql = "SELECT * FROM Win32_ShadowCopy"
        for disk in self.wmi.query(wql):
            print (disk)

        #print(self.wmi.Win32_ShadowCopy[0])
        #or disk in self.wmi.Win32_ShadowCopy:
        #    print (disk)
