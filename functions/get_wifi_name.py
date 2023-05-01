import subprocess
import re

def getWifiList():
    output = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'])
    wifi_list = []
    for line in output.splitlines():
        if b'SSID' in line:
            try:
                wifi_list.append(line.decode().strip())
            except:
                pass
    wifi_dict = {}
    ssid_regex = re.compile(r'SSID\s+(\d+)\s+:\s+(.*)')
    bssid_regex = re.compile(r'BSSID\s+(\d+)\s+:\s+(.*)')
    for line in wifi_list:
        ssid_match = ssid_regex.match(line)
        bssid_match = bssid_regex.match(line)
        if ssid_match:
            ssid_name = ssid_match.group(2)
            wifi_dict[ssid_name] = ''
        elif bssid_match:
            bssid_value = bssid_match.group(2)
            prev_ssid_name = list(wifi_dict.keys())[-1]
            wifi_dict[prev_ssid_name] = bssid_value
    return wifi_dict