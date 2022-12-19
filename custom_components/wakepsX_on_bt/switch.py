"""Support for wakeps4 on bt."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity

from .const import (
    CONF_ADAPTER,
    CONF_DUALSHOCK_BT_ADDRESS,
    CONF_PLAYSTATION4_BT_ADDRESS,
    DOMAIN,
    SERVICE_SEND_MAGIC_PACKET,
    WOBTPS4_PREFIX,
)

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ADAPTER): cv.string,
        vol.Required(CONF_DUALSHOCK_BT_ADDRESS): cv.string,
        vol.Required(CONF_PLAYSTATION4_BT_ADDRESS): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a wakeps4 on bt."""
    adapter = config.get(CONF_ADAPTER)
    dsbt_address = config.get(CONF_DUALSHOCK_BT_ADDRESS)
    ps4bt_address = config.get(CONF_PLAYSTATION4_BT_ADDRESS)

    add_entities([WOBTPS4Switch(hass, adapter, ps4bt_address, dsbt_address)], True)


class WOBTPS4Switch(SwitchEntity):
    """Representation of a wakeps4 on bt switch."""

    def __init__(self, hass, adapter, ps4bt_address, dsbt_address):
        """Initialize the WOL switch."""
        self._hass = hass
        self._adapter = adapter
        self._ps4bt_address = ps4bt_address
        self._dsbt_address = dsbt_address
        self._state = False  # always False, we can not know

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    @property
    def name(self):
        """Return the name of the switch."""
        return WOBTPS4_PREFIX + self._ps4bt_address

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._hass.services.call(
            DOMAIN,
            SERVICE_SEND_MAGIC_PACKET,
            {
                CONF_ADAPTER: self._adapter,
                CONF_DUALSHOCK_BT_ADDRESS: self._dsbt_address,
                CONF_PLAYSTATION4_BT_ADDRESS: self._ps4bt_address,
            },
        )

    def turn_off(self, **kwargs):
        """Bt can not turn off Ps4."""
        return

    def update(self):
        """No way to check (yet)."""
        return
