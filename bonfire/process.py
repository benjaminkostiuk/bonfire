import wmi
import os
import time
# from pywinauto import Application
# from pywinauto.findwindows import find_windows, find_elements
# from pywinauto import mouse, keyboard

from .config import config
from .utils import format_process_name

# Return a map of whitelisted applications currently running
def find_running_apps():
    c = wmi.WMI()
    app_map = {}
    for process in c.Win32_Process():
        if process.Name in config().whitelist and process.Name not in app_map:
            instances = []
            if process.Name == 'chrome.exe':
                pass
                #instances = get_all_chrome_tabs()

            clean_name = config().whitelist[process.Name].get('name', None)
            app_map[process.Name] = {
                'process': process.Name,
                'path': process.ExecutablePath,
                'name': clean_name if clean_name else format_process_name(process.Name),
                'instances': instances,
                'instance_count': 1 if not instances else len(instances)
            }
    return app_map

# Get the number of chrome instances and the url of all tabs
# def get_all_chrome_tabs():
#     instances = []
#     app = Application(backend='uia')
#     for process in find_windows(title_re=".*Chrome.*"):
#         # Connect to the instance and focus the tab
#         app.connect(handle=process)
#         instance = app.window(handle=process)
#         instance.set_focus()

#         urls = []
#         # Assumes there are no duplicated tabs
#         while True:
#             # Get the url in the search field
#             url = instance.child_window(title="Address and search bar", control_type="Edit").get_value()
#             if url in urls:
#                 break
            
#             urls.append(url)
#             keyboard.send_keys("^{TAB}")    # Switch tabs

#         instances.append(urls)
#     return instances

# Open an application by starting the app from its executable path
def open_application(process, process_details):
    # Spawn a detached thread to open the application
    # Must pass 'null' as arg to spawnl to prevent crash
    
    #for _ in range(process_details['instance_count']):
    os.spawnl(os.P_DETACH, process_details['path'], 'null')  
    # # Handle special cases
    # if process == 'chrome.exe':
    #     open_chrome_instances(process_details['instances'])

# Open all instances of chrome with the proper urls
# def open_chrome_instances(instances):
#     time.sleep(1)
#     instance_index = 0
#     app = Application(backend='uia')
#     for process in find_windows(title_re=".*Chrome.*"):
#         if instance_index >= len(instances):
#             break

#         # Connect to the instance and focus the tab
#         app.connect(handle=process)
#         instance = app.window(handle=process)
#         instance.set_focus()
#         time.sleep(0.5)

#         # Check that the url is empty
#         url = instance.child_window(title="Address and search bar", control_type="Edit").get_value()
#         if url != '':
#             continue
#         # Fill first tab
#         keyboard.send_keys("{}".format(instances[instance_index][0]), pause=0.0)
#         time.sleep(0.1)
#         keyboard.send_keys("{ENTER}")
#         # Fill rest of tabs
#         for i in range(1, len(instances[instance_index])):
#             keyboard.send_keys("^T")    # Create a new tab tabs
#             time.sleep(0.1)
#             keyboard.send_keys("{}".format(instances[instance_index][i]), pause=0.0)
#             time.sleep(0.1)
#             keyboard.send_keys("{ENTER}")
#         instance_index += 1