import subprocess, sys, os, ctypes, time
import urllib.request
import threading
from init import *

import hashlib
from proxy import *


class SHA256:
    def calc(file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()


    def verify(file_path, expected_hash):
        """Verify if the file's SHA-256 hash matches the expected hash."""
        calculated_hash = SHA256.calc(file_path)
        return calculated_hash == expected_hash


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("You need to run this as admin.")
        input()
        sys.exit()
    init()
    cert_path = os.path.join(dir, 'vault\\cert.cer')
    


    if SHA256.verify(trustcert, "4130fa595c107211549c8be551754822aae811a2857ce39863e41eb5e3662bbf"):

        if not os.path.exists(cert_path):
            def run():
                with open("logs\\proxy.log", "w") as stdout_file, open("logs\\proxy_errors.log", "w") as stderr_file:
                    subprocess.run([os.path.join(os.path.dirname(__file__), mitmdump)], stdout=stdout_file, stderr=stderr_file)
            t = threading.Thread(target=run)
            t.start()
            
            time.sleep(2.5)
            
            ProxyManager.set_and_enable_proxy()
            ProxyActions.reload()
            
            print('Downloading certificate...')
            try:
                urllib.request.urlretrieve("http://mitm.it/cert/cer", cert_path)
                if os.path.exists(cert_path):
                    print("Successfully downloaded cert!")
                ProxyManager.disable_proxy()
                ProxyActions.reload()
            except Exception as e:
                print(f"Failed to download the certificate: {e}")
                input()
                ProxyManager.disable_proxy()
                ProxyActions.reload()
                time.sleep(0.25)
                sys.exit()
                
                
        os.system(f"{trustcert} -path={cert_path}")
        subprocess.run(["certutil.exe", "-addstore", "root", cert_path]) # Add Cert
        time.sleep(2.5)
        print("You may close this window now.")
        sys.exit()
    else:
        print('ALERT: INCORRECT HASH DETECTED')
        input()
        sys.exit()
