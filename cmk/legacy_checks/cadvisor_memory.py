#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json
from collections.abc import Iterable, Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
)
from cmk.legacy_includes.mem import check_memory_element

Section = Mapping[str, float]


def parse_cadvisor_memory(string_table: StringTable) -> Section:
    memory_info = json.loads(string_table[0][0])
    parsed: dict[str, float] = {}
    for memory_name, memory_entries in memory_info.items():
        if len(memory_entries) != 1:
            continue
        try:
            parsed[memory_name] = float(memory_entries[0]["value"])
        except KeyError:
            continue
    return parsed


def _output_single_memory_stat(
    memory_value: float, output_text: str, metric_name: str | None = None
) -> Iterable[Result | Metric]:
    infotext = output_text % (memory_value / 1024)
    yield Result(state=State.OK, summary=infotext)
    if metric_name:
        yield Metric(metric_name, memory_value)


def discover_cadvisor_memory(section: Section) -> DiscoveryResult:
    if section:
        yield Service()


def check_cadvisor_memory(section: Section) -> CheckResult:
    # Checking for Container
    if "memory_usage_container" in section:
        memory_used = section["memory_usage_container"]
        memory_total = section["memory_usage_pod"]
        infotext_extra = " (Parent pod memory usage)"

    # Checking for Pod
    else:
        memory_used = section["memory_usage_pod"]
        if section.get("memory_limit", 0):
            memory_total = section["memory_limit"]
            infotext_extra = ""
        else:
            memory_total = section["memory_machine"]
            infotext_extra = " (Available Machine Memory)"

    status, infotext, perfdata = check_memory_element(
        "Usage", memory_used, memory_total, None, metric_name="mem_used"
    )
    yield Result(state=State(status), summary=f"{infotext}{infotext_extra}")
    for metric_tuple in perfdata:
        yield Metric(metric_tuple[0], metric_tuple[1])

    # the cAdvisor does not provide available (total) memory of the following
    yield from _output_single_memory_stat(section["memory_rss"], "Resident size: %s kB")

    yield from _output_single_memory_stat(section["memory_cache"], "Cache: %s kB", "mem_lnx_cached")

    yield from _output_single_memory_stat(section["memory_swap"], "Swap: %s kB", "swap_used")


agent_section_cadvisor_memory = AgentSection(
    name="cadvisor_memory",
    parse_function=parse_cadvisor_memory,
)


check_plugin_cadvisor_memory = CheckPlugin(
    name="cadvisor_memory",
    service_name="Memory",
    discovery_function=discover_cadvisor_memory,
    check_function=check_cadvisor_memory,
)
