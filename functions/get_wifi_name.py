import re
from subprocess import run, PIPE

def getWifiList():
    output = run(['sudo', 'iw', 'dev', 'wlan0', 'scan'], capture_output=True)
    ssid_s = re.findall(r"\tSSID.*", output.stdout.decode())
    bss_s = re.findall(r"BSS (?:[0-9a-fA-F]:?){12}.*", output.stdout.decode())
    channel_s = re.findall(r".*DS Parameter set: channel.*", output.stdout.decode())
    wifi_dict = {}
    for i in range(len(ssid_s)):
        ssid = ssid_s[i].replace("\tSSID: ", "")
        bss = re.findall(r"(?:[0-9a-fA-F]:?){12}", bss_s[i])
        channel = channel_s[i].replace("\tDS Parameter set: channel ", "")
        wifi_dict[bss[0]] = { ssid : channel }
    return wifi_dict