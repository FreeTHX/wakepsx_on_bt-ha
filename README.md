# wakepsx_on_bt Wake Playstation (Ps3, Ps4, Ps5) on BlueTooth

### HASS Integration
Copy the custom_components folder to get it install under '/config/custom_components/wakepsx_on_bt/'.  
Edit your configuration.yaml file.

```YAML
# Wake PsX On BT
wakepsx_on_bt:

switch:
  - platform: wakepsx_on_bt
    adapter: 'hci0'
    dsbt_address: xx:xx:xx:xx:xx:xx
    psxbt_address: xx:xx:xx:xx:xx:xx
```

### Get device BT addresses
To get the required bluetooth addr, go to the Home Assistant Developer-Tools, Service page.  
Plug the SixAxis, DualShock or DualSense controler and run the wakepsx_on_bt: get_bt_addr service.  
Info will be accessible in the ServiceResponse.  