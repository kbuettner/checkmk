#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping, Sequence

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
)

Section = Mapping[str, Mapping[str, str]]


def parse_tcw241_digital(string_table: Sequence[StringTable]) -> Section:
    """
    parse string_table data and create list of namedtuples for 4 digital sensors.

    expected string_table structure:
        list of digital sensor descriptions and states:
            [description1, description2, description3, description4]
            [input state1, input state2, input state3, input state4]

    converted to dictionary:
        {
            1: { description1: state1 }
            ...
            4: { description4: state4 }
        }

    :param string_table: parsed snmp data
    :return: list of namedtuples for digital sensors
    """
    try:
        descriptions, states = string_table[0][0], string_table[1][0]
    except IndexError:
        return {}

    info_dict: dict[str, dict[str, str]] = {}
    for index, (description, state) in enumerate(zip(descriptions, states)):
        # if state is '1', the sensor is 'open'
        sensor_state = "open" if state == "1" else "closed"

        info_dict[str(index + 1)] = {"description": description, "state": sensor_state}
    return info_dict


def check_tcw241_digital(item: str, section: Section) -> CheckResult:
    """
    Check sensor if it is open or closed

    :param item: sensor number
    :param section: dictionary with digital sensor description and state (open/close)
    :return: status
    """
    if not (info_dict := section.get(item)):
        return
    yield Result(
        state=State.OK if info_dict.get("state") == "open" else State.CRIT,
        summary="[{}] is {}".format(
            info_dict.get("description"),
            info_dict.get("state"),
        ),
    )


def discover_teracom_tcw241_digital(section: Section) -> DiscoveryResult:
    yield from (Service(item=item) for item in section)


snmp_section_teracom_tcw241_digital = SNMPSection(
    name="teracom_tcw241_digital",
    detect=contains(".1.3.6.1.2.1.1.1.0", "Teracom"),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.38783.3.2.2.3",
            oids=["1.0", "2.0", "3.0", "4.0"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.38783.3.3.3",
            oids=["1.0", "2.0", "3.0", "4.0"],
        ),
    ],
    parse_function=parse_tcw241_digital,
)

check_plugin_teracom_tcw241_digital = CheckPlugin(
    name="teracom_tcw241_digital",
    service_name="Digital Sensor %s",
    discovery_function=discover_teracom_tcw241_digital,
    check_function=check_tcw241_digital,
)
