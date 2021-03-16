import wmi
import ctypes
import platform
import os

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

        #Текущий ID ShadowCopy
        self.current_shadowcopy_id=""
        #Текущая директория для монтирования
        self.current_dirtomount = ""

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

    def __id_shadowcopy_normalise(self,id="error"):
        #нормализуем id теневой копии '{00000000-0000-0000-0000-000000000000}'
        id = id.upper()
        if id[0] != "{":
            id = "{" + id
        if len(id) == 37:
            id = id + "}"

        if (len(id) == 38 and id[0] == "{" and id[37] == "}" and id[9] == "-" and id[14] == "-" and id[19] == "-" and id[24] == "-" ):
            return id
        else:
            print("Attention!! The ID shadowcopy does not match the format {00000000-0000-0000-0000-000000000000}")
            return False

    def __drive_letter_normalise(self,drive_letter="error"):
        #Функция нормазиования имени диска
        drive_letter=drive_letter.upper()
        if len(drive_letter) >=4 or len(drive_letter) == 0:
            print("Attention!! The drive letter is not specified correctly(For example, C:, C:\\)")
            return False

        if len(drive_letter) == 1:
            drive_letter = "{0}:\\".format(drive_letter)

        if len(drive_letter) == 2 and drive_letter[1] != ":":
            print("Attention!! The drive letter is not specified correctly(For example, C:, C:\\)")
            return False
        elif len(drive_letter) == 2 and drive_letter[1] == ":":
            drive_letter="{0}\\".format(drive_letter)

        if (len(drive_letter) == 3 and (drive_letter[1] != ":" or drive_letter[2] != "\\")):
            print("Attention!! The drive letter is not specified correctly(For example, C:, C:\\)")
        return drive_letter

    def shadowcopy_description_return_value(self,return_code=-1):
        # Возращает описание результата работы метода Create класса Win32_ShadowCopy
        # https://docs.microsoft.com/en-us/previous-versions/windows/desktop/vsswmi/create-method-in-class-win32-shadowcopy
        value=("Success.", "Access denied.", "Invalid argument.", "Specified volume not found.", "Specified volume not supported.", "Unsupported shadow copy context.", "Insufficient storage.", "Volume is in use.", "Maximum number of shadow copies reached.", "Another shadow copy operation is already in progress.", "Shadow copy provider vetoed the operation.", "Shadow copy provider not registered.", "Shadow copy provider failure.", "Unknown error.")
        if return_code >= 0 and return_code <= 13 :
            return value[return_code]
        return return_code

    def create_shadowcopy_by_drive(self,drive_letter="error"):
        # Создает shadowcopy по полученной литере диска, возвращает False или ShadowCopy ID
        drive_letter=self.__drive_letter_normalise(drive_letter)
        if not(drive_letter):
            return False
        #проверяем можем ли мы выполнить shadowcopy (Является ли предложеный диск, диском с типом FS - NTFS)
        if self.system_disk.isdisjoint({drive_letter[0:2]}):
            print("Attention!! There is no way to create a ShadowCopy on disk ", drive_letter[0:2], " . Аvailable", self.system_disk)
            return False
        self.create_shadowcopy=self.wmi.Win32_ShadowCopy.Create(Volume=drive_letter, Context="ClientAccessible")
        self.current_shadowcopy_id=self.create_shadowcopy[1]
        if self.create_shadowcopy[0] != 0:
            print(self.shadowcopy_description_return_value(self.create_shadowcopy[0]))
        self.get_shadowcopys_id()
        return self.current_shadowcopy_id

    def delete_shadowcopy_by_id(self,id):
        #Удаляем теневую копию
        id=self.__id_shadowcopy_normalise(id)
        if not(id):
            return False
        # Обновляем список доступных копий
        self.get_shadowcopys_id()
        if self.shadowcopys_id.isdisjoint({id}):
            print("Attention!! You can't delete it. ", id, " - id was not found . Аvailable", self.shadowcopys_id)
            return False
        return self.wmi.Win32_ShadowCopy(ID=id)[0].Delete_()

    def delete_current_shadowcopy(self):
        #Удаляем текущую теневую копию
        return self.delete_shadowcopy_by_id(self.current_shadowcopy_id)

    def get_information_shadowcopy_by_id(self, id):
        id=self.__id_shadowcopy_normalise(id)
        if not(id):
            return False
        # Обновляем список доступных копий
        self.get_shadowcopys_id()
        if self.shadowcopys_id.isdisjoint({id}):
            print("Attention!! ", id, " - id was not found . Аvailable", self.shadowcopys_id)
            return False
        return self.wmi.Win32_ShadowCopy(ID=id)[0]

        #for shadowcopy in self.wmi.Win32_ShadowCopy():
        #    self.shadowcopys_id.add(shadowcopy.ID)
        #return self.shadowcopys_id

    def __test_dir_name_to_mount(self,dir="error"):
        dir=os.path.normpath(dir)
        if os.path.isdir(dir):
            print("Attention!! Cannot mount to an existing directory ", dir)
            return False
        if not(os.path.isabs(dir)):
            print("Attention!! Not the correct path ", dir)
            return False
        if not(os.path.isdir(os.path.split(dir)[0])):
            print("Attention!! The mount directory is not available ", os.path.split(dir)[0])
            return False
        return "\\\\?\\" + dir

    def mount_shadowcopy_by_id(self, id="error", dirtomount="error"):
        #Монтированеи в каталог теневой копии
        dirtomount=self.__test_dir_name_to_mount(dirtomount)
        id=self.__id_shadowcopy_normalise(id)
        if not(id):
            return False
        self.get_shadowcopys_id()
        if self.shadowcopys_id.isdisjoint({id}):
            print("Attention!! ", id, " - id was not found . Аvailable", self.shadowcopys_id)
            return False

        if dirtomount != False:
            mklink = ctypes.windll.LoadLibrary("kernel32.dll")
            mklink.CreateSymbolicLinkW(dirtomount, self.wmi.Win32_ShadowCopy(ID=id)[0].VolumeName, 1)
            self.current_dirtomount = dirtomount
            return True
        else:
            return False

    def unmount_current_shadowcopy(self):
        #отмонтируем текущую теневую копию копию
        if os.path.exists(self.current_dirtomount):
            os.unlink(self.current_dirtomount)
            return True
        else:
            return False

    def delete_all_shadowcopys(self):
        #Удаляем все доступные теневые копии
        self.get_shadowcopys_id()
        for shadowcopy_id in self.shadowcopys_id:
            self.wmi.Win32_ShadowCopy(ID=shadowcopy_id)[0].Delete_()
        return True


