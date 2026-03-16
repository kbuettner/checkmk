#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# This check verifies a given NFS export is registered with mountd.
# Optionally we can add tracking of allowed clients and filesystem ID.

# Agent info
# [['/mirrored/data/recording', '172.0.0.0/255.0.0.0']]


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


def parse_nfsexports(string_table: StringTable) -> StringTable:
    return string_table


def discover_nfsexports(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[0].startswith("/"):
            yield Service(item=line[0])


def check_nfsexports(item: str, section: StringTable) -> CheckResult:
    if len(section) == 0:
        yield Result(
            state=State.CRIT,
            summary="exports defined but no exports found in export list. Daemons might not be working",
        )
        return

    for line in section:
        if item == line[0]:
            yield Result(state=State.OK, summary="export is active")
            return

    yield Result(state=State.CRIT, summary="export not found in export list")


agent_section_nfsexports = AgentSection(
    name="nfsexports",
    parse_function=parse_nfsexports,
)

check_plugin_nfsexports = CheckPlugin(
    name="nfsexports",
    service_name="NFS export %s",
    discovery_function=discover_nfsexports,
    check_function=check_nfsexports,
)
