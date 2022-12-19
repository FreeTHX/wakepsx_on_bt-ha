# wakepsX_on_bt Wake ps3,ps4,ps5 on BlueTooth

### HASS Integration
Copy the custom_components folder to get it install under '/config/custom_components/wakepsX_on_bt/'.  
Edit your configuration.yaml file.

```YAML
# Wake PsX On BT
wakepsX_on_bt:

switch:
  - platform: wakepsX_on_bt
    adapter: 'hci0'
    dsbt_address: xx:xx:xx:xx:xx:xx
    psXbt_address: xx:xx:xx:xx:xx:xx
```
