#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# example output
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.2.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.2.2 2
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.3.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.3.2 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.4.1 "Controller A"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.4.2 "Controller B"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.5.1 "10.20.30.41"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.5.2 "10.20.30.42"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.7.1 "CT_SC4020"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.7.2 "CT_SC4020"


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import compellent_dev_state_map, DETECT_DELL_COMPELLENT


def discover_dell_compellent_controller(section: StringTable) -> DiscoveryResult:
    for number, *_rest in section:
        yield Service(item=number)


def check_dell_compellent_controller(item: str, section: StringTable) -> CheckResult:
    for number, status, name, addr, model in section:
        if number == item:
            state, state_readable = compellent_dev_state_map(status)
            yield Result(state=state, summary=f"Status: {state_readable}")
            yield Result(state=State.OK, summary=f"Model: {model}, Name: {name}, Address: {addr}")


def parse_dell_compellent_controller(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_compellent_controller = SimpleSNMPSection(
    name="dell_compellent_controller",
    detect=DETECT_DELL_COMPELLENT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.11000.2000.500.1.2.13.1",
        oids=["2", "3", "4", "5", "7"],
    ),
    parse_function=parse_dell_compellent_controller,
)


check_plugin_dell_compellent_controller = CheckPlugin(
    name="dell_compellent_controller",
    service_name="Controller %s",
    discovery_function=discover_dell_compellent_controller,
    check_function=check_dell_compellent_controller,
)
