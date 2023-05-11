import os
import subprocess
import re
def crack_wifi(ssid,bssid):
    ssid = ssid.replace(' ', '_')
    command = f'aircrack-ng -w /opt/wordlists/rockyou.txt {ssid}_{bssid}.cap'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode())
    out  = re.findall("KEY.*" ,output.decode())
    print(out)
    return out[0]