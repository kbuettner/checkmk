#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


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


def discover_unitrends_replication(section: StringTable) -> DiscoveryResult:
    seen: set[str] = set()
    for _application, _result, _complete, target, _instance in section:
        if target not in seen:
            seen.add(target)
            yield Service(item=target)


def check_unitrends_replication(item: str, section: StringTable) -> CheckResult:
    # this never gone be a blessed check :)
    replications = [x for x in section if x[3] == item]
    if len(replications) == 0:
        yield Result(state=State.UNKNOWN, summary="No Entries found")
        return
    not_successfull = [x for x in replications if x[1] != "Success"]
    if len(not_successfull) == 0:
        yield Result(state=State.OK, summary="All Replications in the last 24 hours Successfull")
        return
    messages = []
    for _application, result, _complete, target, instance in not_successfull:
        messages.append(f"Target: {target}, Result: {result}, Instance: {instance}  ")
    # TODO: Maybe a good place to use multiline output here
    yield Result(state=State.CRIT, summary="Errors from the last 24 hours: " + "/ ".join(messages))


def parse_unitrends_replication(string_table: StringTable) -> StringTable:
    return string_table


agent_section_unitrends_replication = AgentSection(
    name="unitrends_replication",
    parse_function=parse_unitrends_replication,
)

check_plugin_unitrends_replication = CheckPlugin(
    name="unitrends_replication",
    service_name="Replicaion %s",
    discovery_function=discover_unitrends_replication,
    check_function=check_unitrends_replication,
)
