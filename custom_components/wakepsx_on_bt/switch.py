"""Support for wakepsx on bt."""
import logging

import voluptuous as vol

from homeassistant.components.switch import (
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    SwitchEntity,
)
from .const import (
    CONF_ADAPTER,
    CONF_CONTROLER_BT_ADDRESS,
    CONF_PLAYSTATION_BT_ADDRESS,
    DOMAIN,
    SERVICE_SEND_MAGIC_PACKET,
    WOBTPSX_PREFIX,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PARENT_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ADAPTER): cv.string,
        vol.Required(CONF_CONTROLER_BT_ADDRESS): cv.string,
        vol.Required(CONF_PLAYSTATION_BT_ADDRESS): cv.string,
        vol.Optional(CONF_NAME, default=""): cv.string,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up a wake psx on bt switch."""
    adapter: str | None = config.get(CONF_ADAPTER)
    dsbt_address: int | None = config.get(CONF_CONTROLER_BT_ADDRESS)
    psxbt_address: str | None = config.get(CONF_PLAYSTATION_BT_ADDRESS)
    name: str | None = config.get(CONF_NAME)
    add_entities(
        [
            WOBTPSXSwitch(
                hass,
                adapter,
                psxbt_address,
                dsbt_address,
                name
            )
        ],
        False
    )

class WOBTPSXSwitch(SwitchEntity):
    """Representation of a wakepsx on bt switch."""

    def __init__(self,
                 hass: HomeAssistant,
                 adapter: str,
                 psxbt_address: str,
                 dsbt_address: str,
                 name: str | None = None,
    ) -> None:
        """Initialize the WOL switch."""
        self._hass = hass
        self._adapter = adapter
        self._psxbt_address = psxbt_address
        self._dsbt_address = dsbt_address
        self._state = False  # always False, we can not know
        if name is None or not name :
            self._attr_name = WOBTPSX_PREFIX + dr.format_mac(self._psxbt_address)
        else:
            self._attr_name = name
        self._attr_unique_id = WOBTPSX_PREFIX + dr.format_mac(self._psxbt_address)
        self._attr_assumed_state = False
        self._attr_should_poll = False
        self._attr_icon = "mdi:sony-playstation"
        
    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    @property
    def name(self):
        """Return the name of the switch."""
        return self._attr_name

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._hass.services.call(
            DOMAIN,
            SERVICE_SEND_MAGIC_PACKET,
            {
                CONF_ADAPTER: self._adapter,
                CONF_CONTROLER_BT_ADDRESS: self._dsbt_address,
                CONF_PLAYSTATION_BT_ADDRESS: self._psxbt_address,
            },
        )

    def turn_off(self, **kwargs):
        """Bt can not turn off PsX."""
        return

    def update(self):
        """No way to check (yet)."""
        return
