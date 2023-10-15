import os
import requests

dir = os.path.join(os.getenv('APPDATA'), 'BypasserApplication')
tools_dir = os.path.join(dir, "tools")
vault_dir = os.path.join(dir, "vault")

mitmdump = os.path.join(tools_dir, "mitmdump.exe")
mitmproxy = os.path.join(tools_dir, "mitmproxy.exe")
trustcert = os.path.join(tools_dir, "TrustCert.exe")
trustcert2 = os.path.join(tools_dir, "TrustCert.pdb")



def init():
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(tools_dir):
        os.mkdir(tools_dir)
    if not os.path.exists(vault_dir):
        os.mkdir(vault_dir)
        
    if not os.path.exists("logs"):
        os.mkdir("logs")

    download_if_not_exists("https://raw.githubusercontent.com/NotJINXZ/RobloxUWP-UpdateBypass/main/tools/mitmdump.exe", mitmdump)
    download_if_not_exists("https://raw.githubusercontent.com/NotJINXZ/RobloxUWP-UpdateBypass/main/tools/mitmproxy.exe", mitmproxy)
    download_if_not_exists("https://raw.githubusercontent.com/NotJINXZ/RobloxUWP-UpdateBypass/main/tools/TrustCert.exe", trustcert)
    download_if_not_exists("https://raw.githubusercontent.com/NotJINXZ/RobloxUWP-UpdateBypass/main/tools/TrustCert.pdb", trustcert2)

def download_if_not_exists(url, filename, use_proxy=False):
    proxies = None
    if not use_proxy:
        proxies = {'http': None, 'https': None}

    if not os.path.exists(filename):
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)