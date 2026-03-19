#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import DETECT_OPENMANAGE
from cmk.plugins.lib.temperature import check_temperature, TempParamType

_SENSOR_STATES = {
    1: "other",
    2: "unknown",
    10: "failed",
}


def dell_om_sensors_item(name: str) -> str:
    return name.replace("Temp", "").strip()


def discover_dell_om_sensors(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[3]:
            yield Service(item=dell_om_sensors_item(line[3]))


def check_dell_om_sensors(item: str, params: TempParamType, section: StringTable) -> CheckResult:
    for (
        idx,
        sensor_state_str,
        reading,
        location_name,
        dev_crit_str,
        dev_warn_str,
        dev_warn_lower_str,
        dev_crit_lower_str,
    ) in section:
        if item == idx or dell_om_sensors_item(location_name) == item:
            sensor_state = int(sensor_state_str)
            if sensor_state in _SENSOR_STATES:
                yield Result(state=State.CRIT, summary=f"Sensor is: {_SENSOR_STATES[sensor_state]}")
                return

            temp = int(reading) / 10.0

            dev_warn, dev_crit, dev_warn_lower, dev_crit_lower = (
                float(v) / 10 if v else None
                for v in [dev_warn_str, dev_crit_str, dev_warn_lower_str, dev_crit_lower_str]
            )
            if not dev_warn_lower:
                dev_warn_lower = dev_crit_lower
            if not dev_warn:
                dev_warn = dev_crit

            dev_levels = (
                (dev_warn, dev_crit) if dev_warn is not None and dev_crit is not None else None
            )
            dev_levels_lower = (
                (dev_warn_lower, dev_crit_lower)
                if dev_warn_lower is not None and dev_crit_lower is not None
                else None
            )

            yield from check_temperature(
                temp,
                params,
                unique_name=f"dell_om_sensors_{item}",
                value_store=get_value_store(),
                dev_levels=dev_levels,
                dev_levels_lower=dev_levels_lower,
            )
            return


def parse_dell_om_sensors(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_om_sensors = SimpleSNMPSection(
    name="dell_om_sensors",
    detect=DETECT_OPENMANAGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.1.700.20.1",
        oids=["2", "5", "6", "8", "10", "11", "12", "13"],
    ),
    parse_function=parse_dell_om_sensors,
)

check_plugin_dell_om_sensors = CheckPlugin(
    name="dell_om_sensors",
    service_name="Temperature %s",
    discovery_function=discover_dell_om_sensors,
    check_function=check_dell_om_sensors,
    check_ruleset_name="temperature",
    check_default_parameters={"levels": (50.0, 60.0)},
)
