#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Sequence

from cmk.agent_based.v2 import (
    all_of,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    equals,
    get_value_store,
    OIDEnd,
    Service,
    SNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType

# .1.3.6.1.4.1.14848.2.1.7.1.2.1 -0.0008 Volt --> ...
# .1.3.6.1.4.1.14848.2.1.9.1.2.1 -2472        --> ...

# suggested by customer

Section = dict[str, float]


def parse_etherbox2_temp(string_table: Sequence[StringTable]) -> Section:
    # We have to use xxx.7.1.2.a to know if a temperature sensor
    # is connected:
    # - if oid(xxx.7.1.2.{a}) == 5.fff and oid(xxx.7.1.2.{a+1}) == 2.fff
    #   then a temperature sensor is connected to oid(xxx.9.1.2.{(a+1)/2})
    #   (a = 1, 3, 5, ...)
    # - otherwise there's no sensor connected.
    # Furthermore we cannot only use xxx.9.1.2.{a} < 0 (or something like that)
    # because the temperature can drop below 0.
    parsed: Section = {}
    sensor_indicators, sensors = string_table
    for sensor_index, sensor in enumerate(sensors):
        indicator_index = 2 * sensor_index
        if (
            float((sensor_indicators[indicator_index][0].split("Volt")[0]).strip()) > 4
            and float((sensor_indicators[indicator_index + 1][0].split("Volt")[0]).strip()) > 1
        ):
            parsed[f"Sensor {sensor[0]}"] = float(sensor[1]) / 10

    return parsed


def discover_etherbox2_temp(section: Section) -> DiscoveryResult:
    yield from (Service(item=sensor) for sensor in section)


def check_etherbox2_temp(item: str, params: TempParamType, section: Section) -> CheckResult:
    if item in section:
        yield from check_temperature(
            reading=section[item],
            params=params,
            unique_name=f"etherbox2_{item}",
            value_store=get_value_store(),
        )


snmp_section_etherbox2_temp = SNMPSection(
    name="etherbox2_temp",
    detect=all_of(
        equals(".1.3.6.1.2.1.1.1.0", ""), contains(".1.3.6.1.4.1.14848.2.1.1.1.0", "Version 1.2")
    ),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.14848.2.1.7.1",
            oids=["2"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.14848.2.1.9.1",
            oids=[OIDEnd(), "2"],
        ),
    ],
    parse_function=parse_etherbox2_temp,
)

check_plugin_etherbox2_temp = CheckPlugin(
    name="etherbox2_temp",
    service_name="Temperature %s",
    discovery_function=discover_etherbox2_temp,
    check_function=check_etherbox2_temp,
    check_ruleset_name="temperature",
    check_default_parameters={
        "levels": (30.0, 35.0),
    },
)
