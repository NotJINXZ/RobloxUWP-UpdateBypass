import os, sys
import subprocess
import time
import winreg as reg
from mitmproxy import http
import json
import platform
from init import *
from proxy import *

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )

def run_mitmdump():
    if not os.path.exists("logs"):
        os.mkdir("logs")
    try:
        with open("logs\\proxy.log", "w") as stdout_file, open("logs\\proxy_errors.log", "w") as stderr_file:
            subprocess.run([mitmdump, '-s', resource_path("./proxy.py")], stdout=stdout_file, stderr=stderr_file)
    except Exception as e:
        print("Error running mitmdump:", str(e))


if __name__ == '__main__':
    if platform.system() != "Windows":
        print(f"Only windows is supported. Your platfrom: [{platform.system()}]")
        input()
        sys.exit()
    init()

    
    # Set and enable the proxy
    if ProxyManager.set_and_enable_proxy():
        print("Now capturing traffic...")
    else:
        print("Failed to set and enable proxy.")

    # Reload proxy settings
    ProxyActions.reload()
    time.sleep(.25)

    print("Running!")
    run_mitmdump()

    
    ProxyManager.disable_proxy()
    ProxyActions.reload()