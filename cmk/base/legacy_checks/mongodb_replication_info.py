#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# <<<mongodb_replication_info>>>
# <json>
# {
#   "tFirst": 1566891670,
#   "tLast": 1566891670,
#   "now": 1568796109,
#   "usedBytes": 9765922,
#   "logSizeBytes": 16830742272
# }


import json
from collections.abc import Iterable, Mapping

from cmk.agent_based.legacy.v0_unstable import LegacyCheckDefinition
from cmk.agent_based.v2 import render

check_info = {}

Section = Mapping


def parse_mongodb_replication_info(string_table):
    """
    :param string_table: dictionary with replication string_table from local.oplog.rs
    :return: dict
    """
    if string_table:
        return json.loads(str(string_table[0][0]))
    return {}


def discover_mongodb_replication_info(section: Section) -> Iterable[tuple[None, dict]]:
    if section:
        yield None, {}


def check_mongodb_replication_info(_no_item, _no_params, info_dict):
    """
    just outputting long output and performance data for now.
    :param item:
    :param params:
    :param status_dict:
    :return:
    """
    oplog_size = "Oplog size: {} of {} used".format(
        _bytes_human_readable(info_dict, "usedBytes"),
        _bytes_human_readable(info_dict, "logSizeBytes"),
    )

    try:
        timestamp_first_operation = info_dict.get("tFirst", 0)
        timestamp_last_operation = info_dict.get("tLast", 0)
        time_difference_sec = timestamp_last_operation - timestamp_first_operation
        time_diff = "Time difference: %s between the first and last operation on oplog" % (
            render.timespan(time_difference_sec)
        )
    except TypeError:
        time_diff = "Time difference: n/a"

    yield 0, oplog_size
    yield 0, time_diff
    yield 0, _long_output(info_dict), _generate_performance_data(info_dict)


def _generate_performance_data(info_dict):
    """
    create all performance data
    :param collection_dict: dictionary holding collections information
    :return:
    """
    log_size_bytes = _get_as_int(info_dict, "logSizeBytes")
    used_bytes = _get_as_int(info_dict, "usedBytes")
    timestamp_first_operation = _get_as_int(info_dict, "tFirst")
    timestamp_last_operation = _get_as_int(info_dict, "tLast")
    time_difference_sec = timestamp_last_operation - timestamp_first_operation

    perfdata = []
    perfdata.append(("mongodb_replication_info_log_size", log_size_bytes))
    perfdata.append(("mongodb_replication_info_used", used_bytes))
    perfdata.append(("mongodb_replication_info_time_diff", time_difference_sec))
    return perfdata


def _long_output(info_dict):
    timestamp_first_operation = _timestamp_human_readable(info_dict, "tFirst")
    timestamp_last_operation = _timestamp_human_readable(info_dict, "tLast")
    timestamp_on_node = _timestamp_human_readable(info_dict, "now")
    time_difference_sec = _calc_time_diff(info_dict.get("tLast"), info_dict.get("tFirst"))

    # output per collection
    long_output = []
    long_output.append("Operations log (oplog):")
    long_output.append(
        "- Total amount of space allocated: %s" % _bytes_human_readable(info_dict, "logSizeBytes")
    )
    long_output.append(
        "- Total amount of space currently used: %s" % _bytes_human_readable(info_dict, "usedBytes")
    )
    long_output.append("- Timestamp for the first operation: %s" % timestamp_first_operation)
    long_output.append("- Timestamp for the last operation: %s" % timestamp_last_operation)
    long_output.append(
        "- Difference between the first and last operation: %s" % time_difference_sec
    )
    long_output.append("")
    long_output.append("- Current time on host: %s" % timestamp_on_node)
    return "\n" + "\n".join(long_output)


def _bytes_human_readable(data, key):
    try:
        return render.bytes(int(data.get(key)))
    except (TypeError, ValueError):
        return "n/a"


def _timestamp_human_readable(data, key):
    try:
        return render.datetime(int(data.get(key)))
    except (TypeError, ValueError):
        return "n/a"


def _calc_time_diff(value1, value2):
    try:
        return render.timespan(value1 - value2)
    except TypeError:
        return "n/a"


def _get_as_int(data, key):
    try:
        return int(data.get(key))
    except (KeyError, ValueError):
        return 0


check_info["mongodb_replication_info"] = LegacyCheckDefinition(
    name="mongodb_replication_info",
    parse_function=parse_mongodb_replication_info,
    service_name="MongoDB Replication Info",
    discovery_function=discover_mongodb_replication_info,
    check_function=check_mongodb_replication_info,
)
