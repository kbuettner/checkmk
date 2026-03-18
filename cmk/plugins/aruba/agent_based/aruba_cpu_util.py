#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import time
from collections.abc import Mapping
from typing import TypedDict

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    StringTable,
)
from cmk.plugins.lib.cpu_util import check_cpu_util


def parse_aruba_cpu_util(string_table: StringTable) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for description, raw_cpu_util in string_table:
        try:
            parsed.setdefault(description, float(raw_cpu_util))
        except ValueError:
            pass
    return parsed


class ArubaCpuUtilParams(TypedDict, total=False):
    levels: tuple[float, float]
    average: int


# no get_parsed_item_data because the cpu utilization can be exactly 0 for some devices, which would
# result in "UNKN - Item not found in monitoring data", because parsed[item] evaluates to False
def check_aruba_cpu_util(
    item: str, params: ArubaCpuUtilParams, section: Mapping[str, float]
) -> CheckResult:
    measured_cpu_util = section.get(item)
    if measured_cpu_util is None:
        return
    yield from check_cpu_util(
        util=measured_cpu_util,
        params=params,
        value_store=get_value_store(),
        this_time=time.time(),
    )


def discover_aruba_cpu_util(
    section: Mapping[str, float],
) -> DiscoveryResult:
    yield from (Service(item=item) for item in section)


snmp_section_aruba_cpu_util = SimpleSNMPSection(
    name="aruba_cpu_util",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.14823"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.14823.2.2.1.1.1.9.1",
        oids=["2", "3"],
    ),
    parse_function=parse_aruba_cpu_util,
)


check_plugin_aruba_cpu_util = CheckPlugin(
    name="aruba_cpu_util",
    service_name="CPU utilization %s",
    discovery_function=discover_aruba_cpu_util,
    check_function=check_aruba_cpu_util,
    check_ruleset_name="cpu_utilization_multiitem",
    check_default_parameters={
        "levels": (80.0, 90.0),
    },
)
