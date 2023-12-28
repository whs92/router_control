## Control a VPN client with a physical switch

I would like to provide a physical switch that people can use to switch the VPN on the router from the UK to DE so that the chromecast connected to the projector can be switched between different countries. 

Assuming I make switch connected to something that is in the same network as the router I need some code that will allow me to interact with the router vpn clients. 

## Packet sniffing to find api

The ASUS router has no public API. I found out the required REST API calls using a packet sniffer on my phone while running the ASUS router app. 

To turn off the VPN client and effectively connect to DE use 
```
    '{ 
     "vpnc_proto": "disable",
     "vpnc_pptp_options_x": "",
     "vpn_clientx_eas": "",
     "vpn_client_unit": "",
     "vpnc_pppoe_username": "",
     "vpnc_pppoe_passwd": "",
     "vpnc_heartbeat_x": "", 
     "action_mode": "apply" 
     }' 
```

To turn on vpn client 4 which is pre-configured to connect to the UK use:

```
    '{ 
     "vpnc_proto": "openvpn",
     "vpnc_pptp_options_x": "auto",
     "vpn_clientx_eas": "4,",
     "vpn_client_unit": "4",
     "vpn_client4_username": "my_user","vpn_client4_password": "my_pass", 
     "action_mode": "apply" 
     }'
```

After issuing the command, you have to apply it with:

```
    '{
     "action_mode": "apply",
     "rc_service": "restart_vpncall;"
     }'
```
