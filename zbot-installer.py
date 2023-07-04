# (Unofficial?) zBot installer. Made by terminite (@terminite)
# FOR ZBOT PRO ONLY!!!!!!!!
import os

print("zBot Installer - by terminite")

try:
    import requests
except ModuleNotFoundError:
    print("Requests is not installed. Installing...")
    os.system("py -m pip install requests")
    os.system("pip install requests")
    print("\nFinished. Please restart the installer.")
    print("If this error reoccurs, something has gone wrong. There may be something wrong with your Python installation.")
    os.system("pause")
    exit()

scriptdir = os.path.dirname(os.path.realpath(__file__))

gddir = None
move = False

def directory_setup():
    global gddir
    dircheck = input("Would you like to use the default installation directory? (y/n): ")
    if dircheck == "y":
        gddir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash"
    else:
        gddir = input("Geometry Dash Directory (with executable): ")
        if not os.path.isdir(gddir):
            print("The Geometry Dash Directory you entered is not a directory. Please try again.")
            os.system("pause")
            directory_setup()
        else:
            if gddir == "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash":
                print("That's the default directory. But okay...")
            if os.path.isfile(os.path.join(gddir, "GeometryDash.exe")):
                print("Found GeometryDash.exe")
            else:
                print("Could not find GeometryDash.exe. Please try again.")
                os.system("pause")
                directory_setup()
    print(f"Using Geometry Dash Directory: {gddir}\n")
    start()

def start():
    global move
    if os.path.isfile(os.path.join(gddir, "hackpro.dll")):
        print("Found hackpro.dll. Checking if it's Mega Hack v7...")
        if os.path.isfile(os.path.join(gddir, "hackproldr.dll")):
            print("Mega Hack v7 found. Please uninstall Mega Hack v7 before installing zBot.")
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
    print("Downloading zBot...")
    url = "https://zbot.figmentcoding.me/static/archive/zBot%20v2.0.0.dll"

    req = requests.get(url)
    if req.status_code != 200:
        print("Could not download zBot. Please try again later.")
        exit()
    else:
        if not os.path.isdir(os.path.join(gddir, "adaf-dll")):
            print("adaf-dll not found, creating...")
            os.mkdir(os.path.join(gddir, "adaf-dll"))
        with open(os.path.join(gddir, "adaf-dll", "zBot v2.0.0.dll"), "wb") as f:
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
    dllloader = 'https://github.com/adafcaefc/GDDllLoader/releases/download/v2/GDDLLLoader.dll'
    extensionfile = 'https://github.com/adafcaefc/GDDllLoader/releases/download/v2/libExtensions.dll'
    req = requests.get(dllloader)
    if req.status_code != 200:
        print("Could not download GDDLLLoader. Please try again later.")
        exit()
    else:
        with open(os.path.join(gddir, "GDDLLLoader.dll"), "wb") as f:
            f.write(req.content)
            print(f"Installed GDDLLLoader inside of {gddir}")
    req = requests.get(extensionfile)
    if req.status_code != 200:
        print("Could not download libExtensions. Please try again later.")
        exit()
    else:
        with open(os.path.join(gddir, "libExtensions.dll"), "wb") as f:
            f.write(req.content)
            print(f"Installed libExtensions inside of {gddir}")

    print("GDDLLLoader installation complete. Starting key process...\n")
    check_key()

def check_key():
    url = f'https://zbot.figmentcoding.me/get-guid/'
    key = input("Please enter your zBot key. This can be found in your email at checkout: ")
    req = requests.get(url + key)
    if req.status_code != 200:
        print("Invalid key. Please try again.\n")
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
            print("Key already in use. If you believe this is a mistake, please contact 'zBot Support' inside of the Discord.")
            check_key()

def finished_setup():
    print("zBot installation is now complete. Please open Geometry Dash.")
    print("\nYou might've gotten a virus detection by now. Please whitelist it and continue. If you don't, zBot will not work.\n")
    print("If you have any more issues, please read #faq in the Discord server.")
    os.system("pause")

directory_setup()