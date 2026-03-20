#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    StringTable,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType


def discover_ipr400_temp(section: StringTable) -> DiscoveryResult:
    if len(section) > 0:
        yield Service(item="Ambient")


def check_ipr400_temp(item: str, params: TempParamType, section: StringTable) -> CheckResult:
    yield from check_temperature(
        reading=int(section[0][0]),
        params=params,
        unique_name=f"ipr400_temp_{item}",
        value_store=get_value_store(),
    )


def parse_ipr400_temp(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_ipr400_temp = SimpleSNMPSection(
    name="ipr400_temp",
    parse_function=parse_ipr400_temp,
    detect=startswith(".1.3.6.1.2.1.1.1.0", "ipr voip device ipr400"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.27053.1.4.5",
        oids=["9"],
    ),
)

check_plugin_ipr400_temp = CheckPlugin(
    name="ipr400_temp",
    service_name="Temperature %s ",
    discovery_function=discover_ipr400_temp,
    check_function=check_ipr400_temp,
    check_ruleset_name="temperature",
    check_default_parameters={
        "levels": (30.0, 40.0),  # reported temperature seems to be near room temperature usually
    },
)
