#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping

from cmk.agent_based.v2 import (
    all_of,
    any_of,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    endswith,
    exists,
    get_value_store,
    OIDEnd,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType

# No factory default because of different defaultlevels
carel_temp_defaultlevels: Mapping[str, tuple[float, float]] = {
    "Room": (30, 35),
    "Outdoor": (60, 70),
    "Delivery": (60, 70),
    "Cold Water": (60, 70),
    "Hot Water": (60, 70),
    "Cold Water Outlet": (60, 70),
    "Circuit 1 Suction": (60, 70),
    "Circuit 2 Suction": (60, 70),
    "Circuit 1 Evap": (60, 70),
    "Circuit 2 Evap": (60, 70),
    "Circuit 1 Superheat": (60, 70),
    "Circuit 2 Superheat": (60, 70),
    "Cooling Set Point": (60, 70),
    "Cooling Prop. Band": (60, 70),
    "Cooling 2nd Set Point": (60, 70),
    "Heating Set Point": (60, 70),
    "Heating 2nd Set Point": (60, 70),
    "Heating Prop. Band": (60, 70),
}

Section = Mapping[str, float]


def carel_sensors_parse(string_table: StringTable) -> Section:
    oid_parse = {
        "1.0": "Room",
        "2.0": "Outdoor",
        "3.0": "Delivery",
        "4.0": "Cold Water",
        "5.0": "Hot Water",
        "7.0": "Cold Water Outlet",
        "10.0": "Circuit 1 Suction",
        "11.0": "Circuit 2 Suction",
        "12.0": "Circuit 1 Evap",
        "13.0": "Circuit 2 Evap",
        "14.0": "Circuit 1 Superheat",
        "15.0": "Circuit 2 Superheat",
        "20.0": "Cooling Set Point",
        "21.0": "Cooling Prop. Band",
        "22.0": "Cooling 2nd Set Point",
        "23.0": "Heating Set Point",
        "24.0": "Heating 2nd Set Point",
        "25.0": "Heating Prop. Band",
    }

    parsed: dict[str, float] = {}
    for oidend, value in string_table:
        sensor_name = oid_parse.get(oidend)
        if sensor_name is not None and value not in {None, "0", "-9999"}:
            parsed[sensor_name] = float(value) / 10

    return parsed


snmp_section_carel_sensors = SimpleSNMPSection(
    name="carel_sensors",
    parse_function=carel_sensors_parse,
    detect=all_of(
        any_of(contains(".1.3.6.1.2.1.1.1.0", "pCO"), endswith(".1.3.6.1.2.1.1.1.0", "armv4l")),
        exists(".1.3.6.1.4.1.9839.1.1.0"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9839.2.1",
        oids=[OIDEnd(), "2"],
    ),
)


def discover_carel_sensors_temp(section: Section) -> DiscoveryResult:
    for sensor in section:
        levels = carel_temp_defaultlevels[sensor]
        yield Service(item=sensor, parameters={"levels": levels})


def check_carel_sensors_temp(item: str, params: TempParamType, section: Section) -> CheckResult:
    if item in section:
        yield from check_temperature(
            reading=section[item],
            params=params,
            unique_name=f"carel_sensors_temp_{item}",
            value_store=get_value_store(),
        )


check_plugin_carel_sensors = CheckPlugin(
    name="carel_sensors",
    service_name="Temperature %s",
    discovery_function=discover_carel_sensors_temp,
    check_function=check_carel_sensors_temp,
    check_ruleset_name="temperature",
    check_default_parameters={},
)
