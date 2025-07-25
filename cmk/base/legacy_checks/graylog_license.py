#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import time

from cmk.agent_based.legacy.v0_unstable import check_levels, LegacyCheckDefinition
from cmk.agent_based.v2 import render
from cmk.base.check_legacy_includes.graylog import (
    handle_iso_utc_to_localtimestamp,
    parse_graylog_agent_data,
)

check_info = {}

# <<<graylog_license>>>
# {"status": [{"violated": true,"expired": false,"expiration_upcoming":
# false,"expired_since": "PT0S","expires_in": "PT550H17.849S","trial":
# true,"license": {"version": 2,"id":
# "*********************************","issuer": "Graylog, Inc.","subject":
# "/license/enterprise","audience": {"company": "MYCOMPANY","name":
# "****************************","email":
# "*******************************"},"issue_date":
# "2019-09-23T05:00:00Z","expiration_date":
# "2019-10-24T04:59:59Z","not_before_date": "2019-09-23T05:00:00Z","trial":
# true,"enterprise": {"cluster_ids":
# ["***********************************************"],"number_of_nodes":
# 2147483647,"require_remote_check": true,"allowed_remote_check_failures":
# 120,"traffic_limit": 5368709120,"traffic_check_range":
# "PT720H","allowed_traffic_violations": 5,"expiration_warning_range":
# "PT240H"},"expired": false},"traffic_exceeded": false,"cluster_not_covered":
# false,"nodes_exceeded": false,"remote_checks_failed": true,"valid": false}]}


def inventory_graylog_license(parsed):
    license_state = parsed.get("status")
    if license_state is not None:
        return [(None, {})]
    return []


def check_graylog_license(_no_item, params, parsed):
    license_state = parsed.get("status")
    if license_state is None:
        return

    # if no enterprise licence could be found
    if not license_state:
        yield params.get("no_enterprise"), "No enterprise license found"
        return

    license_data = license_state[0]

    for key, infotext, expected in [
        ("expired", "Is expired", "False"),
        ("violated", "Is violated", "False"),
        ("valid", "Is valid", "True"),
        ("traffic_exceeded", "Traffic is exceeded", "False"),
        ("cluster_not_covered", "Cluster is not covered", "False"),
        ("nodes_exceeded", "Nodes exceeded", "False"),
        ("remote_checks_failed", "Remote checks failed", "False"),
    ]:
        data = license_data.get(key)
        if data is not None:
            state = 0
            if str(data) != expected:
                state = params.get(key, 2)

            yield state, f"{infotext}: {_handle_readable_output(data)}"

    traffic_limit = license_data.get("license", {}).get("enterprise", {}).get("traffic_limit")
    if traffic_limit is not None:
        yield 0, "Traffic limit: %s" % render.bytes(traffic_limit)

    expires = license_data.get("license", {}).get("expiration_date")
    if expires is not None:
        timestamp = handle_iso_utc_to_localtimestamp(expires)
        time_to_expiration = int(timestamp) - time.time()
        warn, crit = params.get("expiration", (None, None))
        yield check_levels(
            time_to_expiration,
            None,
            (None, None, warn, crit),
            human_readable_func=render.time_offset,
            infoname="Expires in",
        )

    for key in [
        ("subject"),
        ("trial"),
    ]:
        value = license_data.get("license", {}).get(key)
        if value is not None:
            yield (
                0,
                "{}: {}".format(" ".join(key.split("_")).title(), _handle_readable_output(value)),
            )

    remote_check = license_data.get("license", {}).get("enterprise", {}).get("require_remote_check")
    if remote_check is not None:
        yield 0, "Requires remote checks: %s" % _handle_readable_output(remote_check)


def _handle_readable_output(value):
    return str(value).replace("False", "no").replace("True", "yes")


check_info["graylog_license"] = LegacyCheckDefinition(
    name="graylog_license",
    parse_function=parse_graylog_agent_data,
    service_name="Graylog License",
    discovery_function=inventory_graylog_license,
    check_function=check_graylog_license,
    check_ruleset_name="graylog_license",
    check_default_parameters={
        "no_enterprise": 0,
        "valid": 2,
        "cluster_not_covered": 1,
        "traffic_exceeded": 1,
        "violated": 2,
        "nodes_exceeded": 1,
        "expired": 2,
        "remote_checks_failed": 1,
    },
)
