
import requests
import ubinascii
import network
import socket
from time import sleep
import machine
from machine import Pin
from utime import sleep

# Login Info
from secrets import *

# Pin defintions
green = Pin(2, Pin.OUT)
red = Pin(3, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
green.on()
red.on()

# VPN Client number to enable
vpn_num = 4

print("Waiting For Switch")


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
    
def apply_vpn_change(token):
    #restart vpn service

    payload = '{ "action_mode": "apply", "rc_service": "restart_vpncall;" }")'
    headers = {
        'user-Agent': "asusrouter-Android-DUTUtil-1.0.0.245",
        'cookie': 'asus_token={}'.format(token),
    }
    try:
        r = requests.post(url='http://{}/applyapp.cgi'.format(asus_ip), data=payload, headers=headers)
        return r.json()
    except:
        print('Failed')
    
    
def turn_off_vpn(token):
    
    #Turn off vpn
    payload = '{ "vpnc_proto": "disable", "vpnc_pptp_options_x": "", "vpn_clientx_eas": "", "vpn_client_unit": "", "vpnc_pppoe_username": "", "vpnc_pppoe_passwd": "", "vpnc_heartbeat_x": "", "action_mode": "apply" };")'
    headers = {
        'user-Agent': "asusrouter-Android-DUTUtil-1.0.0.245",
        'cookie': 'asus_token={}'.format(token),
    }
    try:
        r = requests.post(url='http://{}/applyapp.cgi'.format(asus_ip), data=payload, headers=headers)
        return r.json()
    except:
        print('Failed in turn off vpn')
    

def turn_on_vpn(token, vpn_num: int):
    
    payload = '{ "vpnc_proto": "openvpn", "vpnc_pptp_options_x": "auto", "vpn_clientx_eas": "'+str(vpn_num)+',", "vpn_client_unit": "'+str(vpn_num)+'", "vpn_client'+str(vpn_num)+'_username": "'+ str(nord_user)+ '", "vpn_client'+str(vpn_num)+'_password": "'+ str(nord_pw)+ '", "action_mode": "apply" };")'
    headers = {
        'user-Agent': "asusrouter-Android-DUTUtil-1.0.0.245",
        'cookie': 'asus_token={}'.format(token),
    }
    try:
        r = requests.post(url='http://{}/applyapp.cgi'.format(asus_ip), data=payload, headers=headers)
        print(r.json())
    except:
        print('Failed in turn on vpn')
    
def get_vpn_status(token, vpn_num: int):
    
    payload = "hook=nvram_get(vpn_clientx_eas);')"
    headers = {
        'user-Agent': "asusrouter-Android-DUTUtil-1.0.0.245",
        'cookie': 'asus_token={}'.format(token),
    }
    try:
        r = requests.post(url='http://{}/appGet.cgi'.format(asus_ip), data=payload, headers=headers)
        response = r.json()
        

        if "vpn_clientx_eas" in response:
            if response["vpn_clientx_eas"] ==str(vpn_num)+",":
                
                return 1
            else:
                
                return 0
    except:
        print('Failed in get vpn status')
        return 2
    

# Connect to the WLAN
try:
    connect()
except KeyboardInterrupt:
    machine.reset()
    
# Connect to the router
string_bytes = account.encode('ascii')
base64_bytes = ubinascii.b2a_base64(string_bytes)
login = base64_bytes.decode('ascii')

url = 'http://{}/login.cgi'.format(asus_ip)
payload = "login_authorization=" + login
headers = {
    'user-agent': "asusrouter-Android-DUTUtil-1.0.0.245"
}
r = requests.post(url=url, data=payload, headers=headers)
token = r.json()['asus_token']
print(f"Connected to Router. The token is: {token}")

status= get_vpn_status(token,vpn_num)

if status == 1:
    print("VPN is On")
    red.off()

else:
    print("VPN is Off")
    green.off()
    
sleep(1)
# When the switch is connected the VPN should be on. 
# When the switch is disconnected the VPN should be off
while True:

    status= get_vpn_status(token,vpn_num)
    if button.value() == 1 and status == 0:
        # Request to turn the VPN ON

        red.off()
        green.off()
        
        turn_on_vpn(token, vpn_num)
        apply_vpn_change(token)
        while get_vpn_status(token,vpn_num) == 0:
            sleep(1)

        print("VPN is On")
        red.off()
        green.on()
    elif button.value() == 0 and status == 1:
        # Request to turn the VPN OFF

        red.off()
        green.off()
        
        turn_off_vpn(token)
        apply_vpn_change(token)
        while get_vpn_status(token,vpn_num) == 1:
            sleep(1)

        print("VPN is Off")
        green.off()
        red.on()

    sleep(0.1)
        

        
        
            
