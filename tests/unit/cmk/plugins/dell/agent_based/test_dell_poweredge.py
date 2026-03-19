#!/usr/bin/env python3
# Copyright (C) 2021 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.agent_based.v2 import Metric, Result, State
from cmk.plugins.dell.agent_based.dell_poweredge_amperage import (
    check_dell_poweredge_amperage_current,
    check_dell_poweredge_amperage_power,
)


def test_check_dell_poweredge_amperage_power_state_simple() -> None:
    section = [["1", "3", "2", "3", "168", "26", "My-test-item", "980", "896"]]
    result = list(check_dell_poweredge_amperage_power("My-test-item", section))
    results = [r for r in result if isinstance(r, Result)]
    metrics = [r for r in result if isinstance(r, Metric)]
    assert results[0].state == State.OK
    assert "168 Watt" in results[0].summary
    assert "(upper limits 896/980)" in results[0].summary
    assert metrics[0].name == "power"
    assert metrics[0].value == 168.0


def test_check_dell_poweredge_amperage_current_state_unknown() -> None:
    # StateSettings == "1" means unknown
    section = [["1", "1", "1", "2", "", "23", "My-test-item", "", ""]]
    result = list(check_dell_poweredge_amperage_current("My-test-item", section))
    results = [r for r in result if isinstance(r, Result)]
    assert results[0].state == State.UNKNOWN
    assert "unknown" in results[0].summary.lower()


def test_check_dell_poweredge_amperage_power_not_found() -> None:
    section = [["1", "3", "2", "3", "168", "26", "Other-item", "980", "896"]]
    result = list(check_dell_poweredge_amperage_power("My-test-item", section))
    results = [r for r in result if isinstance(r, Result)]
    assert results[0].state == State.UNKNOWN
    assert "not found" in results[0].summary.lower()
