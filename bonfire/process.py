import wmi
import os
from time import sleep
from .config import config

# Models information about applications
class Application:
    def __init__(self, process_name, exec_path):
        self.process_name = process_name
        self.exec_path = exec_path

    # Class constructor to build an application from a dict
    @classmethod
    def fromdict(cls, datadict):
        return cls(datadict['process_name'], datadict['exec_path'])

    # Add a to_dict() method

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)


# Return a map of whitelisted applications currently running
def find_running_apps():
    c = wmi.WMI()
    app_map = {}
    for process in c.Win32_Process():
        if process.Name in config().whitelist and process.Name not in app_map:
            print("Found {}".format(process.Name))
            # Change this to use Application
            app_map[process.Name] = process.ExecutablePath
    return app_map

# Open an application by starting the app from its executable path
def open_application(app_name, exec_path):
    print('Starting app {}'.format(app_name))
    os.startfile('C:\\Users\\benko\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe')
    sleep(100)