"""
Component to wake up a ps3,ps4,ps5 using BT

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/wakepsX_on_bt/
"""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import wakepsXonbt

from .const import (
    CONF_ADAPTER,
    CONF_CONTROLER_BT_ADDRESS,
    CONF_PLAYSTATION_BT_ADDRESS,
    DOMAIN,
    SERVICE_GET_BT_ADDR,
    SERVICE_SEND_MAGIC_PACKET,
)

_LOGGER = logging.getLogger(__name__)

WAKEPSX_ON_BT_SEND_MAGIC_PACKET_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADAPTER): cv.string,
        vol.Required(CONF_CONTROLER_BT_ADDRESS): cv.string,
        vol.Required(CONF_PLAYSTATION_BT_ADDRESS): cv.string,
    }
)
GET_BT_ADDR_SCHEMA = vol.Schema({})


def setup(hass, config):
    """Set up the wakepsX on bt component."""

    def send_magic_packet(call):
        """Send magic packet to wake up a psX."""
        adapter = call.data.get(CONF_ADAPTER)
        bt_address_tospoof = call.data.get(CONF_CONTROLER_BT_ADDRESS)
        psX_address_toconnectto = call.data.get(CONF_PLAYSTATION_BT_ADDRESS)

        if wakepsXonbt.send_magic_packet(
            adapter, psX_address_toconnectto, bt_address_tospoof
        ):
            _LOGGER.info(
                "Send magic packet to psX %s (spoofing controler: %s) from %s",
                psX_address_toconnectto,
                bt_address_tospoof,
                adapter,
            )
        else:
            _LOGGER.error("Adapter %s does not yet support addr spoofing", adapter)

    def get_bt_addr(call):
        """Get Bluetooth addresses via USB"""
        res = wakepsXonbt.get_bt_addr()
        if res is None:
            _LOGGER.error("Unable to find SixAxis / DualShock / DualSense on USB")
            return ""

        """Display result in Log (WARNING)"""
        _LOGGER.warning(res)
        return res

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_MAGIC_PACKET,
        send_magic_packet,
        schema=WAKEPSX_ON_BT_SEND_MAGIC_PACKET_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN, SERVICE_GET_BT_ADDR, get_bt_addr, schema=GET_BT_ADDR_SCHEMA
    )

    return True
