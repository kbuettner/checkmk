#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# .1.3.6.1.4.1.10876.2.1.1.1.1.2.1 Fan1 Fan Speed
# .1.3.6.1.4.1.10876.2.1.1.1.1.2.2 Fan2 Fan Speed
# ...
# .1.3.6.1.4.1.10876.2.1.1.1.1.2.6 Vcore Voltage
# .1.3.6.1.4.1.10876.2.1.1.1.1.2.7 CPU VTT Voltage
# .1.3.6.1.4.1.10876.2.1.1.1.1.3.1 0
# ...
# .1.3.6.1.4.1.10876.2.1.1.1.1.4.1 3760
# ...
# .1.3.6.1.4.1.10876.2.1.1.1.1.11.1 RPM
# ...
# .1.3.6.1.4.1.10876.2.1.1.1.1.11.6 mV
# .1.3.6.1.4.1.10876.2.1.1.1.1.12.1 0
# ...
# .1.3.6.1.4.1.10876.2.2 0
# .1.3.6.1.4.1.10876.2.3 No problem.

# .
#   .--Health--------------------------------------------------------------


from cmk.agent_based.v2 import (
    all_of,
    any_of,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    equals,
    exists,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)

DETECT_SUPERMICRO = any_of(
    equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.311.1.1.3.1.2"),
    all_of(contains(".1.3.6.1.2.1.1.1.0", "linux"), exists(".1.3.6.1.4.1.10876.2.1.1.1.1.2.1")),
)

_STATE_MAP = {0: State.OK, 1: State.WARN, 2: State.CRIT, 3: State.UNKNOWN}


def discover_supermicro_health(section: StringTable) -> DiscoveryResult:
    if section:
        yield Service()


def check_supermicro_health(section: StringTable) -> CheckResult:
    yield Result(state=_STATE_MAP.get(int(section[0][0]), State.UNKNOWN), summary=section[0][1])


def parse_supermicro(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_supermicro = SimpleSNMPSection(
    name="supermicro",
    parse_function=parse_supermicro,
    detect=DETECT_SUPERMICRO,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10876.2",
        oids=["2", "3"],
    ),
)

check_plugin_supermicro = CheckPlugin(
    name="supermicro",
    service_name="Overall Hardware Health",
    discovery_function=discover_supermicro_health,
    check_function=check_supermicro_health,
)

# .
#   .--Sensors------------------------------------------------------------


def discover_supermicro_sensors(section: StringTable) -> DiscoveryResult:
    for name, _sensor_type, _reading, _high, _low, _unit, _status in section:
        yield Service(item=name)


def check_supermicro_sensors(item: str, section: StringTable) -> CheckResult:
    class Type:
        _Fan, Voltage, Temperature, Status = ("0", "1", "2", "3")

    def worst_status(*args: int) -> State:
        order = [0, 1, 3, 2]
        worst = sorted(args, key=lambda x: order[x], reverse=True)[0]
        return _STATE_MAP.get(worst, State.UNKNOWN)

    def expect_order(*args: float) -> int:
        return max(
            abs(x[0] - x[1][0]) for x in enumerate(sorted(enumerate(args), key=lambda x: x[1]))
        )

    for name, sensor_type, reading, high, low, unit, dev_status in section:
        if name == item:
            reading_f = float(reading)
            dev_status_i = int(dev_status)

            crit_upper = warn_upper = None
            status_high = status_low = 0
            if high:
                crit_upper = float(high)
                warn_upper = crit_upper * 0.95
                status_high = expect_order(reading_f, warn_upper, crit_upper)
            if low:
                crit_lower = float(low)
                warn_lower = crit_lower * 1.05
                status_low = expect_order(crit_lower, warn_lower, reading_f)

            perfvar = None
            display_reading: str | float = reading_f

            # normalize values depending on sensor type
            if sensor_type == Type.Temperature:
                unit = f"\N{DEGREE SIGN}{unit}"
                perfvar = "temp"
            elif sensor_type == Type.Voltage:
                if unit == "mV":
                    reading_f, warn_upper, crit_upper = (
                        x / 1000.0  # type: ignore[operator]
                        for x in (reading_f, warn_upper, crit_upper)
                    )
                    display_reading = reading_f
                    unit = "V"
                perfvar = "voltage"
            elif sensor_type == Type.Status:
                display_reading = f"State {int(reading_f)}"
                unit = ""

            yield Result(
                state=worst_status(status_high, status_low, dev_status_i),
                summary=f"{display_reading}{unit}",
            )
            if perfvar:
                yield Metric(perfvar, reading_f, levels=(warn_upper, crit_upper))
            return


def parse_supermicro_sensors(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_supermicro_sensors = SimpleSNMPSection(
    name="supermicro_sensors",
    parse_function=parse_supermicro_sensors,
    detect=DETECT_SUPERMICRO,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10876.2.1.1.1.1",
        oids=["2", "3", "4", "5", "6", "11", "12"],
    ),
)

check_plugin_supermicro_sensors = CheckPlugin(
    name="supermicro_sensors",
    service_name="Sensor %s",
    discovery_function=discover_supermicro_sensors,
    check_function=check_supermicro_sensors,
)

# .
#   .--SMART--------------------------------------------------------------


def format_item_supermicro_smart(name: str) -> str:
    return name.replace(r"\\\\.\\", "")


def discover_supermicro_smart(section: StringTable) -> DiscoveryResult:
    for _serial, name, _status in section:
        yield Service(item=format_item_supermicro_smart(name))


def check_supermicro_smart(item: str, section: StringTable) -> CheckResult:
    # note (only status 0 (OK) and 2 (Crit) are documented.
    # status 3 appears to indicate "unknown" as observed by a user.
    # It's likely - but not verified - that status 1 would indicate a non-
    # critical problem if it's used at all)
    status_map = {"0": State.OK, "1": State.WARN, "2": State.CRIT, "3": State.UNKNOWN}
    for serial, name, status in section:
        if format_item_supermicro_smart(name) == item:
            label_map = {"0": "Healthy", "1": "Warning", "2": "Critical", "3": "Unknown"}
            yield Result(
                state=status_map.get(status, State.UNKNOWN),
                summary=f"(S/N {serial}) {label_map.get(status, 'Unknown')}",
            )
            return


def parse_supermicro_smart(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_supermicro_smart = SimpleSNMPSection(
    name="supermicro_smart",
    parse_function=parse_supermicro_smart,
    detect=DETECT_SUPERMICRO,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10876.100.1.4.1",
        oids=["1", "2", "4"],
    ),
)

check_plugin_supermicro_smart = CheckPlugin(
    name="supermicro_smart",
    service_name="SMART Health %s",
    discovery_function=discover_supermicro_smart,
    check_function=check_supermicro_smart,
)
