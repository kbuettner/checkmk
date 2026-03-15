#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Example output from agent:
# <<<solaris_prtdiag_status>>>
# 0


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


def discover_solaris_prtdiag_status(section: StringTable) -> DiscoveryResult:
    if section:
        yield Service()


def check_solaris_prtdiag_status(section: StringTable) -> CheckResult:
    if not section:
        return

    # 0 No failures or errors are detected in the system.
    # 1 Failures or errors are detected in the system.
    if int(section[0][0]) == 0:
        yield Result(state=State.OK, summary="No failures or errors are reported")
    else:
        yield Result(
            state=State.CRIT,
            summary="Failures or errors are reported by the system. "
            'Please check the output of "prtdiag -v" for details.',
        )


def parse_solaris_prtdiag_status(string_table: StringTable) -> StringTable:
    return string_table


agent_section_solaris_prtdiag_status = AgentSection(
    name="solaris_prtdiag_status",
    parse_function=parse_solaris_prtdiag_status,
)

check_plugin_solaris_prtdiag_status = CheckPlugin(
    name="solaris_prtdiag_status",
    service_name="Hardware Overall State",
    discovery_function=discover_solaris_prtdiag_status,
    check_function=check_solaris_prtdiag_status,
)
