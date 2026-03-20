#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.plugins.salesforce.agent_based.salesforce_instances import (
    check_salesforce_instances,
    discover_salesforce_instances,
    parse_salesforce,
)


def _make_table(*entries: dict[str, object]) -> StringTable:
    return [[json.dumps(e)] for e in entries]


INSTANCE_OK = {
    "key": "NA1",
    "isActive": True,
    "status": "OK",
    "environment": "Production",
    "releaseNumber": "244",
    "releaseVersion": "Spring '24",
}

INSTANCE_MAJOR = {
    "key": "EU2",
    "isActive": True,
    "status": "MAJOR_INCIDENT_CORE",
}

INSTANCE_INACTIVE = {
    "key": "AP1",
    "isActive": False,
    "status": "OK",
}

INSTANCE_NO_KEY = {
    "isActive": True,
    "status": "OK",
}


def test_parse_salesforce_basic() -> None:
    section = parse_salesforce(_make_table(INSTANCE_OK, INSTANCE_MAJOR))
    assert set(section.keys()) == {"NA1", "EU2"}
    assert section["NA1"]["status"] == "OK"


def test_parse_salesforce_skips_entries_without_key() -> None:
    section = parse_salesforce(_make_table(INSTANCE_NO_KEY, INSTANCE_OK))
    assert "NA1" in section
    assert len(section) == 1


def test_discover_yields_only_active_instances() -> None:
    section = parse_salesforce(_make_table(INSTANCE_OK, INSTANCE_MAJOR, INSTANCE_INACTIVE))
    discovered = list(discover_salesforce_instances(section))
    assert all(isinstance(s, Service) for s in discovered)
    assert {s.item for s in discovered} == {"NA1", "EU2"}


@pytest.mark.parametrize(
    "status, expected_state",
    [
        ("OK", State.OK),
        ("MAJOR_INCIDENT_CORE", State.CRIT),
        ("MINOR_INCIDENT_CORE", State.WARN),
        ("MAINTENANCE_CORE", State.OK),
        ("INFORMATIONAL_CORE", State.OK),
        ("MAJOR_INCIDENT_NONCORE", State.CRIT),
        ("MINOR_INCIDENT_NONCORE", State.WARN),
        ("MAINTENANCE_NONCORE", State.OK),
        ("INFORMATIONAL_NONCORE", State.OK),
        ("THIS_IS_NOT_AN_ACTUAL_STATUS", State.UNKNOWN),
    ],
)
def test_check_status_mapping(status: str, expected_state: State) -> None:
    section = parse_salesforce(_make_table({**INSTANCE_OK, "status": status}))
    results = list(check_salesforce_instances("NA1", section))
    assert isinstance(results[0], Result)
    assert results[0].state == expected_state


def test_check_missing_item_yields_nothing() -> None:
    section = parse_salesforce(_make_table(INSTANCE_OK))
    assert list(check_salesforce_instances("NONEXISTENT", section)) == []


def test_check_skips_missing_optional_fields() -> None:
    section = parse_salesforce(_make_table(INSTANCE_MAJOR))
    results = list(check_salesforce_instances("EU2", section))
    # Only the status result, no detail results for missing fields
    assert len(results) == 1
    assert isinstance(results[0], Result)
    assert results[0].state == State.CRIT
