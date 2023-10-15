import winreg as reg
import subprocess
import time
import os
import json
from mitmproxy import http



class ProxyManager:
    reg_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_value_server = "ProxyServer"
    reg_value_enable = "ProxyEnable"
    reg_value_server_data = "localhost:8080"
    reg_value_enable_data = 1
    reg_value_type = reg.REG_SZ

    @staticmethod
    def set_and_enable_proxy():         
        try:
            reg_key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, ProxyManager.reg_key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key_handle, ProxyManager.reg_value_server, 0, ProxyManager.reg_value_type, ProxyManager.reg_value_server_data)
            reg.SetValueEx(reg_key_handle, ProxyManager.reg_value_enable, 0, reg.REG_DWORD, ProxyManager.reg_value_enable_data)
            reg.CloseKey(reg_key_handle)

            return True
        except Exception as e:
            print("Error setting and enabling proxy:", str(e))
            return False

    @staticmethod
    def disable_proxy():
        try:
            reg_key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, ProxyManager.reg_key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key_handle, ProxyManager.reg_value_enable, 0, reg.REG_DWORD, 0)
            reg.CloseKey(reg_key_handle)
            return True
        except Exception as e:
            print("Error disabling proxy:", str(e))
            return False


class ProxyActions:
    @staticmethod
    def reload():
        subprocess.Popen(["start", "ms-settings:network-proxy"], shell=True)
        time.sleep(1)
        os.system("taskkill /f /im SystemSettings.exe > nul 2>&1")


def request(flow: http.HTTPFlow) -> None:
    if flow.request.url == "https://www.roblox.com/mobileapi/check-app-version?appVersion=AppUWPV2.592.586":
        flow.response = http.Response.make(
            200,
            json.dumps({"data":{"UpgradeAction":"None"}}),
            {'Content-Type': 'application/json'}
        )