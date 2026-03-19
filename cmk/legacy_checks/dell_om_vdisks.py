#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# sample agent output:
#
# <<<dell_om_vdisks>>>
# ID                               : 0
# Status                           : Ok
# Name                             : Virtual Disk 0
# State                            : Ready
# Hot Spare Policy violated        : Not Assigned
# Encrypted                        : Not Applicable
# Layout                           : RAID-1
# Size                             : 278.88 GB (299439751168 bytes)
# T10 Protection Information Status : No
# Associated Fluid Cache State     : Not Applicable
# Device Name                      : /dev/sda
# Bus Protocol                     : SAS
# Media                            : HDD
# Read Policy                      : Read Ahead
# Write Policy                     : Write Back
# Cache Policy                     : Not Applicable
# Stripe Element Size              : 64 KB
# Disk Cache Policy                : Unchanged

from collections.abc import Iterable, Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)

Section = Mapping[str, Mapping[str, str]]

_STATUS_MAP: Mapping[str, State] = {
    "ok": State.OK,
    "non-critical": State.WARN,
    "critical": State.CRIT,
    "not found": State.UNKNOWN,
}


def _parse_single_objects(string_table: StringTable) -> Iterable[Mapping[str, str]]:
    current_obj: dict[str, str] = {}
    for line in string_table:
        try:
            idx = line.index(":")
        except ValueError:
            continue
        key = " ".join(line[:idx])
        value = " ".join(line[idx + 1 :])
        if key == "ID" and current_obj:
            yield current_obj
            current_obj = {}
        current_obj[key] = value
    yield current_obj


def parse_dell_om_vdisks(string_table: StringTable) -> Section:
    return {o["ID"]: o for o in _parse_single_objects(string_table)}


def discover_dell_om_vdisks(section: Section) -> DiscoveryResult:
    for key in section:
        yield Service(item=key)


def check_dell_om_vdisks(item: str, section: Section) -> CheckResult:
    if item not in section:
        return
    data = section[item]
    state = _STATUS_MAP.get(data["Status"].lower(), State.CRIT)
    if data["State"] != "Ready":
        state = State.CRIT
    yield Result(
        state=state,
        summary="Device: {}, Status: {}, State: {}, Layout: {}".format(
            data["Device Name"],
            data["Status"],
            data["State"],
            data["Layout"],
        ),
    )


agent_section_dell_om_vdisks = AgentSection(
    name="dell_om_vdisks",
    parse_function=parse_dell_om_vdisks,
)

check_plugin_dell_om_vdisks = CheckPlugin(
    name="dell_om_vdisks",
    service_name="Virtual Disk %s",
    discovery_function=discover_dell_om_vdisks,
    check_function=check_dell_om_vdisks,
)
