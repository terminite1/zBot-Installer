
# (Unofficial?) zBot installer. Made by terminite (@terminite)
# For zBot v2.0.0 and Free Trial | ONLY

import os
import winreg # for hwid checking

print("[***] zBot Installer - by terminite\n\n")

try:
    import requests
except ModuleNotFoundError:
    print("Requests is not installed. Installing...")
    os.system("py -m pip install requests")
    os.system("pip install requests")
    print("\n[!] Finished. Please restart the installer.")
    print("[!] If this error reoccurs, there may be something wrong with your Python installation.")
    os.system("pause")
    exit()

scriptdir = os.path.dirname(os.path.realpath(__file__))

gddir = None
move = False
free = False

usefree = input("[*] Select zBot: Free Trial (1) or Pro (2): ")

def check_free():
    global free
    if usefree == "1":
        free = True
        print("[!] Using free version of zBot.\n")
    directory_setup()

def directory_setup():
    global gddir
    dircheck = input("[*] Select Directory: Default (1) or Custom (2) ")
    if dircheck == "1":
        gddir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash"
    else:
        gddir = input("[*] Geometry Dash Directory (with executable): ")
        if not os.path.isdir(gddir):
            print("[!] The Geometry Dash Directory you entered is not a directory. Please try again.\n")
            directory_setup()
        else:
            if gddir == "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash":
                print("[!] That's the default directory. But okay...")
            if os.path.isfile(os.path.join(gddir, "GeometryDash.exe")):
                print("Found GeometryDash.exe")
            else:
                print("[!] Could not find GeometryDash.exe. Please try again.\n")
                directory_setup()
    print(f"Using Geometry Dash Directory: {gddir}\n")
    start()

def start():
    global move
    if os.path.isfile(os.path.join(gddir, "hackpro.dll")):
        print("Found hackpro.dll. Checking if it's Mega Hack v7...")
        if os.path.isfile(os.path.join(gddir, "hackproldr.dll")):
            print("[!] Mega Hack v7 found. Please uninstall Mega Hack v7 before installing zBot.")
            os.system("pause")
            exit()
        else:
            print("Mega Hack v6 found. Continuing...")
            move = True
            download_zbot()
    else:
        print("Mega Hack not found. Continuing...")
        download_zbot()

def download_zbot():
    global move
    global free

    zbotname = "zBot Free Trial.dll" if free else "zBot Pro v2.0.0.dll"
    print("Downloading zBot...")
    if free:
        url = 'https://cdn.discordapp.com/attachments/883131563552960553/1126171868710305862/zBot_Free_Trial.dll'
        # i uploaded the link myself so it's DDL
        # sry if it looks sketchy
    else:
        url = "https://zbot.figmentcoding.me/static/archive/zBot%20v2.0.0.dll"

    req = requests.get(url)
    if req.status_code != 200:
        print("[!] Could not download zBot. Please try again later.")
        exit()
    else:
        if not os.path.isdir(os.path.join(gddir, "adaf-dll")):
            print("adaf-dll not found, creating...")
            os.mkdir(os.path.join(gddir, "adaf-dll"))
        with open(os.path.join(gddir, "adaf-dll", zbotname), "wb") as f:
            f.write(req.content)
            print(f"Installed zBot inside of {os.path.join(gddir, 'adaf-dll')}")
        if move:
            print("Moving hackpro.dll to adaf-dll...")
            os.rename(os.path.join(gddir, "hackpro.dll"), os.path.join(gddir, "adaf-dll", "hackpro.dll"))
            print("Moved hackpro.dll to adaf-dll")
            print("Installed Mega Hack v6 for GDDLLLoader")
    print("zBot installation complete. Installing GDDLLLoader...\n")
    download_dll_loader()

def download_dll_loader():
    global free
    dllloader = 'https://github.com/adafcaefc/GDDllLoader/releases/download/v2/GDDLLLoader.dll'
    extensionfile = 'https://github.com/adafcaefc/GDDllLoader/releases/download/v2/libExtensions.dll'
    req = requests.get(dllloader)
    if req.status_code != 200:
        print("[!] Could not download GDDLLLoader. Please try again later.")
        exit()
    else:
        with open(os.path.join(gddir, "GDDLLLoader.dll"), "wb") as f:
            f.write(req.content)
            print(f"Installed GDDLLLoader inside of {gddir}")
    req = requests.get(extensionfile)
    if req.status_code != 200:
        print("[!] Could not download libExtensions. Please try again later.")
        exit()
    else:
        with open(os.path.join(gddir, "libExtensions.dll"), "wb") as f:
            f.write(req.content)
            print(f"Installed libExtensions inside of {gddir}")

    print("GDDLLLoader installation complete.\n")
    if free:
        finished_setup()
    else:
        check_key()

def get_hwid():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "System\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001")
    guid = winreg.QueryValueEx(key, "HwProfileGuid")[0]
    return guid

def check_key():
    url = f'https://zbot.figmentcoding.me/get-guid/'
    key = input("[*] Please enter your zBot key. This can be found in your email at checkout: ")
    req = requests.get(url + key)
    if req.status_code != 200:
        print("[!] Invalid key. Please try again.\n")
        check_key()
    else:
        if req.text == 'None':
            print("Valid key! Creating key file...")
            with open(os.path.join(gddir, "key.txt"), "w") as f:
                f.write(key)
                print("Created key file.\n")
                f.close()
                finished_setup()
        else:
            print("[!] Key already in use. checking for HWID match...\n")
            if req.text == get_hwid():
                print("HWID match! Creating key file...")
                with open(os.path.join(gddir, "key.txt"), "w") as f:
                    f.write(key)
                    print("Created key file.\n")
                    f.close()
                    finished_setup()
            else:
                print("[!] HWID mismatch. If you believe this is a mistake, please contact zBot Support in the Discord.\n")
                check_key()

def finished_setup():
    print("[*] zBot installation is now complete. Please open Geometry Dash.")

    print("[!] You might've gotten a virus detection by now. Please whitelist it and continue. If you don't, zBot will not work.\n")
    print("[!] If you have any more issues, please read #faq in the Discord server.\n")
    print("\n[!] Oh, and if you liked the software, please consider leaving a star on the GitHub repo. It helps a lot. Thanks!\n")
    os.system("pause")
    exit()

check_free()