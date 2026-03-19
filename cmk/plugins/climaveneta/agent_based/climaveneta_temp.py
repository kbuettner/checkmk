#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    equals,
    get_value_store,
    OIDEnd,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType

climaveneta_sensors: Mapping[int, str] = {
    1: "Room",
    3: "Outlet Air 1",
    4: "Outlet Air 2",
    5: "Outlet Air 3",
    6: "Outlet Air 4",
    7: "Intlet Air 1",
    8: "Intlet Air 2",
    9: "Intlet Air 3",
    10: "Intlet Air 4",
    11: "Coil 1 Inlet Water",
    12: "Coil 2 Inlet Water",
    13: "Coil 1 Outlet Water",
    14: "Coil 2 Outlet Water",
    23: "Regulation Valve/Compressor",
    24: "Regulation Fan 1",
    25: "Regulation Fan 2",
    28: "Suction",
}


def parse_climaveneta_temp(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_climaveneta_temp = SimpleSNMPSection(
    name="climaveneta_temp",
    parse_function=parse_climaveneta_temp,
    detect=equals(".1.3.6.1.2.1.1.1.0", "pCO Gateway"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9839.2.1",
        oids=[OIDEnd(), "2"],
    ),
)


def discover_climaveneta_temp(section: StringTable) -> DiscoveryResult:
    for sensor_id, value in section:
        sensor_id_int = int(sensor_id.split(".")[0])
        if sensor_id_int in climaveneta_sensors and int(value) > 0:
            yield Service(item=climaveneta_sensors[sensor_id_int])


def check_climaveneta_temp(item: str, params: TempParamType, section: StringTable) -> CheckResult:
    for sensor_id, sensor_value in section:
        sensor_id_int = int(sensor_id.split(".")[0])
        if climaveneta_sensors.get(sensor_id_int) == item:
            yield from check_temperature(
                reading=int(sensor_value) / 10.0,
                params=params,
                unique_name=f"climaveneta_temp_{item}",
                value_store=get_value_store(),
            )
            return


check_plugin_climaveneta_temp = CheckPlugin(
    name="climaveneta_temp",
    service_name="Temperature %s",
    discovery_function=discover_climaveneta_temp,
    check_function=check_climaveneta_temp,
    check_ruleset_name="temperature",
    check_default_parameters={"levels": (28.0, 30.0)},
)
