#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# example output
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.2.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.3.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.5.1 ""
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.6.1 "SAS_EBOD_6G"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.7.1 "EN-SC4020"
# .1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.9.1 "34QLD67"

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


def discover_dell_compellent_enclosure(section: StringTable) -> DiscoveryResult:
    for number, *_rest in section:
        yield Service(item=number)


def check_dell_compellent_enclosure(item: str, section: StringTable) -> CheckResult:
    for number, status, status_message, enc_type, model, serial in section:
        if number == item:
            state, state_readable = compellent_dev_state_map(status)
            yield Result(state=state, summary=f"Status: {state_readable}")
            yield Result(
                state=State.OK, summary=f"Model: {model}, Type: {enc_type}, Service-Tag: {serial}"
            )

            if status_message:
                yield Result(state=state, summary=f"State Message: {status_message}")


def parse_dell_compellent_enclosure(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_compellent_enclosure = SimpleSNMPSection(
    name="dell_compellent_enclosure",
    detect=DETECT_DELL_COMPELLENT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.11000.2000.500.1.2.15.1",
        oids=["2", "3", "5", "6", "7", "9"],
    ),
    parse_function=parse_dell_compellent_enclosure,
)

check_plugin_dell_compellent_enclosure = CheckPlugin(
    name="dell_compellent_enclosure",
    service_name="Enclosure %s",
    discovery_function=discover_dell_compellent_enclosure,
    check_function=check_dell_compellent_enclosure,
)
