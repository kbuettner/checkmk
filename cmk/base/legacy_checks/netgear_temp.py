#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# mypy: disable-error-code="var-annotated"

from cmk.agent_based.legacy.v0_unstable import LegacyCheckDefinition
from cmk.agent_based.v2 import OIDEnd, SNMPTree
from cmk.base.check_legacy_includes.temperature import check_temperature
from cmk.plugins.lib.netgear import DETECT_NETGEAR

check_info = {}

# .1.3.6.1.4.1.4526.10.43.1.8.1.2.1.0 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.1.1 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.1.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.1.2 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.1.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.2.0 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.2.1 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.2.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.2.2 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.2.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.1.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.1.1 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.1.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.1.2 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.1.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.2.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.2.1 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.2.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.2.2 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.2.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.1.0 58 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.1.1 37 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.1.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.1.2 30 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.1.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.2.0 58 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.2.1 37 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.2.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.2.2 30 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.2.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.1.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.1.1 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.1.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.1.2 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.1.2
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.2.0 2 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.2.1 2 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.2.1
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.2.2 2 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.2.2

# BUT (!!)
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.1.0 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.2.2.0 0 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorType.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.1.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.3.2.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorState.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.1.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.4.2.0 1 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorTemperature.2.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.1.0 35 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.1.0
# .1.3.6.1.4.1.4526.10.43.1.8.1.5.2.0 37 --> FASTPATH-BOXSERVICES-PRIVATE-MIB::boxServicesTempSensorsEntry.5.2.0


def parse_netgear_temp(string_table):
    map_types = {
        "1": "fixed",
        "2": "removable",
    }

    versioninfo, sensorinfo = string_table
    parsed = {}
    for oid_end, sensor_ty, sstate, reading_str, reading_str_10 in sensorinfo:
        if versioninfo[0][0].startswith("10."):
            reading = float(reading_str_10)
        else:
            reading = float(reading_str)

        parsed.setdefault(
            "Sensor %s" % oid_end.replace(".", "/"),
            {
                "type": map_types.get(sensor_ty),
                "state": sstate,
                "reading": reading,
            },
        )
    return parsed


def inventory_netgear_temp(parsed):
    return [
        (sensorname, {})
        for sensorname, info in parsed.items()
        if info["state"] not in ["4", "5", "6"]
    ]


def check_netgear_temp(item, params, parsed):
    map_states = {
        "1": (0, "normal"),
        "2": (1, "warning"),
        "3": (2, "critical"),
        "4": (1, "shutdown"),
        "5": (1, "not present"),
        "6": (1, "not operational"),
    }
    if item in parsed:
        data = parsed[item]
        if data["type"]:
            yield 0, "Type: %s" % data["type"]

        dev_status, dev_status_name = map_states[data["state"]]
        yield check_temperature(
            data["reading"],
            params,
            "netgear_temp.%s" % item,
            dev_status=dev_status,
            dev_status_name=dev_status_name,
        )


check_info["netgear_temp"] = LegacyCheckDefinition(
    name="netgear_temp",
    detect=DETECT_NETGEAR,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.4526.10.1.1.1",
            oids=["13"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.4526.10.43.1.8.1",
            oids=[OIDEnd(), "2", "3", "4", "5"],
        ),
    ],
    parse_function=parse_netgear_temp,
    service_name="Temperature %s",
    discovery_function=inventory_netgear_temp,
    check_function=check_netgear_temp,
    check_ruleset_name="temperature",
)
