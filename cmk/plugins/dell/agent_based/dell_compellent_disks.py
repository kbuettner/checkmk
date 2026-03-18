#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# example output
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.2.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.2.2 2
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.3.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.3.2 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.5.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.5.2 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.6.1 ""
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.6.2 ""
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.11.1 1
# .1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.11.2 1

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import compellent_dev_state_map, DETECT_DELL_COMPELLENT

_HEALTH_MAP: Mapping[str, tuple[State, str]] = {
    "1": (State.OK, "healthy"),
    "0": (State.CRIT, "not healthy"),
}


@dataclass(frozen=True)
class DiskInfo:
    status: str
    health: str
    health_message: str
    enclosure: str
    serial: str | None


Section = Mapping[str, DiskInfo]


def parse_dell_compellent_disks(string_table: Sequence[StringTable]) -> Section:
    disk_info = string_table[0]
    disk_serials = dict(string_table[1])

    return {
        disk_name_position: DiskInfo(
            status=status,
            health=health,
            health_message=health_message,
            enclosure=enclosure,
            serial=disk_serials.get(number),
        )
        for number, status, disk_name_position, health, health_message, enclosure in disk_info
    }


def discover_dell_compellent_disks(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_dell_compellent_disks(item: str, section: Section) -> CheckResult:
    if not (disk := section.get(item)):
        return

    state, state_readable = compellent_dev_state_map(disk.status)
    yield Result(state=state, summary=f"Status: {state_readable}")
    yield Result(state=State.OK, summary=f"Location: Enclosure {disk.enclosure}")

    if disk.serial is not None:
        yield Result(state=State.OK, summary=f"Serial number: {disk.serial}")

    if disk.health_message:
        health_state, health_state_readable = _HEALTH_MAP.get(
            disk.health, (State.UNKNOWN, f"unknown[{disk.health}]")
        )
        yield Result(
            state=health_state,
            summary=f"Health: {health_state_readable}, Reason: {disk.health_message}",
        )


snmp_section_dell_compellent_disks = SNMPSection(
    name="dell_compellent_disks",
    detect=DETECT_DELL_COMPELLENT,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.674.11000.2000.500.1.2.14.1",
            oids=["2", "3", "4", "5", "6", "11"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.674.11000.2000.500.1.2.45.1",
            oids=["2", "3"],
        ),
    ],
    parse_function=parse_dell_compellent_disks,
)

check_plugin_dell_compellent_disks = CheckPlugin(
    name="dell_compellent_disks",
    service_name="Disk %s",
    discovery_function=discover_dell_compellent_disks,
    check_function=check_dell_compellent_disks,
)
