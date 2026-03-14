#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, StringTable
from cmk.plugins.vms.agent_based.vms_cpu import check_vms_cpu, discover_vms_cpu, parse_vms_cpu


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        ([["1", "99.17", "0.54", "0.18", "0.00"]], [Service()]),
    ],
)
def test_discover_vms_cpu(
    string_table: StringTable, expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_vms_cpu(string_table)
    result = list(discover_vms_cpu(parsed))
    assert result == expected_discoveries


def test_check_vms_cpu(monkeypatch: pytest.MonkeyPatch) -> None:
    from cmk.plugins.vms.agent_based import vms_cpu

    value_store: dict[str, object] = {}
    monkeypatch.setattr(vms_cpu, "get_value_store", lambda: value_store)

    parsed = parse_vms_cpu([["1", "99.17", "0.54", "0.18", "0.00"]])
    results = list(check_vms_cpu(params={"iowait": None}, section=parsed))

    # Extract Result and Metric objects
    result_objs = [r for r in results if isinstance(r, Result)]
    metric_objs = [m for m in results if isinstance(m, Metric)]

    # Check that we get results for User, System, Wait, Total CPU, and CPU count
    summaries = [r.summary for r in result_objs]
    assert any("User" in s for s in summaries)
    assert any("System" in s for s in summaries)
    assert any("Wait" in s for s in summaries)
    assert any("Total CPU" in s for s in summaries)
    assert any("CPU" in s for s in summaries)

    # Check metrics exist
    metric_names = [m.name for m in metric_objs]
    assert "user" in metric_names
    assert "system" in metric_names
    assert "wait" in metric_names
    assert "cpu_entitlement" in metric_names
