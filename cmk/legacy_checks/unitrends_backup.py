#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Header: Schedule Name, Application Name, Schedule Description, Failures
# <<<unitrends_backup:sep(124)>>>
# HEADER|DMZ-SR01|Hyper-V 2012|DMZ-HV01|0
# rodc2|18761|Incremental|Successful
# rodc2|18761|Incremental|Successful
# owncloud-test|18762|Incremental|Successful


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


def discover_unitrends_backup(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[0] == "HEADER":
            yield Service(item=line[1])


def check_unitrends_backup(item: str, section: StringTable) -> CheckResult:
    message = None
    failures = ""
    details: list[str] = []
    for line in section:
        if line[0] == "HEADER" and message is not None:
            # We are finish collection detail informatoinen
            break

        if message is not None:
            # Collection Backup deatils
            app_type, bid, backup_type, status = line
            details.append(f"Application Type: {app_type} ({bid}), {backup_type}: {status}")
            continue

        if line[0] == "HEADER" and line[1] == item:
            _head, _sched_name, app_name, sched_desc, failures = line
            message = f"{failures} Errors in last 24/h for Application {app_name} ({sched_desc}) "

    if message is not None:
        message += "\n" + "\n".join(details)
        if failures == "0":
            yield Result(state=State.OK, summary=message)
        else:
            yield Result(state=State.CRIT, summary=message)
        return
    yield Result(state=State.UNKNOWN, summary="Schedule not found in Agent Output")


def parse_unitrends_backup(string_table: StringTable) -> StringTable:
    return string_table


agent_section_unitrends_backup = AgentSection(
    name="unitrends_backup",
    parse_function=parse_unitrends_backup,
)

check_plugin_unitrends_backup = CheckPlugin(
    name="unitrends_backup",
    service_name="Schedule %s",
    discovery_function=discover_unitrends_backup,
    check_function=check_unitrends_backup,
)
