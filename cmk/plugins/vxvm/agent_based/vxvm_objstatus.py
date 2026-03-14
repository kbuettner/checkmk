#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Example output:
# <<<vxvm_objstatus>>>
# v datadg lalavol CLEAN DISABLED
# v datadg oravol ACTIVE ENABLED
# v datadg oravol-L01 ACTIVE ENABLED
# v datadg oravol-L02 ACTIVE ENABLED
# v testgroup oravol-L02 ACTIVE ENABLED


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


def vxvm_objstatus_disks(info: StringTable) -> dict[str, list[tuple[str, str, str]]]:
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for dg_type, dg_name, name, admin_state, kernel_state in info:
        if dg_type == "v":
            groups.setdefault(dg_name, []).append((name, admin_state, kernel_state))
    return groups


def discover_vxvm_objstatus(section: StringTable) -> DiscoveryResult:
    yield from (Service(item=k) for k in vxvm_objstatus_disks(section))


def check_vxvm_objstatus(item: str, section: StringTable) -> CheckResult:
    groups = vxvm_objstatus_disks(section)
    volumes = groups.get(item)
    if volumes is not None:
        state = State.OK
        messages = []
        for volume, admin_state, kernel_state in volumes:
            text = []
            error = False
            if admin_state not in {"CLEAN", "ACTIVE"}:
                state = State.CRIT
                text.append(f"{volume}: Admin state is {admin_state}(!!)")
                error = True
            if kernel_state not in {"ENABLED", "DISABLED"}:
                state = State.CRIT
                text.append(f"{volume}: Kernel state is {kernel_state}(!!)")
                error = True
            if error is False:
                text = [f"{volume}: OK"]
            messages.append(", ".join(text))
        yield Result(state=state, summary=", ".join(messages))
        return

    yield Result(state=State.CRIT, summary="Group not found")


def parse_vxvm_objstatus(string_table: StringTable) -> StringTable:
    return string_table


agent_section_vxvm_objstatus = AgentSection(
    name="vxvm_objstatus",
    parse_function=parse_vxvm_objstatus,
)

check_plugin_vxvm_objstatus = CheckPlugin(
    name="vxvm_objstatus",
    service_name="VXVM objstatus %s",
    discovery_function=discover_vxvm_objstatus,
    check_function=check_vxvm_objstatus,
)
