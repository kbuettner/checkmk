#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.plugins.teracom.agent_based.teracom_tcw241_analog import (
    check_tcw241_analog,
    discover_teracom_tcw241_analog,
    parse_tcw241_analog,
)


@pytest.mark.parametrize(
    "info, expected_discoveries",
    [
        (
            [
                [["Tank_Level", "80000", "10000"]],
                [["Motor_Temp", "70000", "37000"]],
                [["Analog Input 3", "60000", "0"]],
                [["Analog Input 4", "60000", "0"]],
                [["48163", "39158", "33", "34"]],
            ],
            [Service(item="1"), Service(item="2")],
        ),
    ],
)
def test_discover_teracom_tcw241_analog(
    info: Sequence[StringTable], expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_tcw241_analog(info)
    result = list(discover_teracom_tcw241_analog(parsed))
    assert sorted(result, key=lambda s: s.item or "") == sorted(
        expected_discoveries, key=lambda s: s.item or ""
    )


@pytest.mark.parametrize(
    "item, info, expected_state, expected_summary_contains",
    [
        (
            "2",
            [
                [["Tank_Level", "80000", "10000"]],
                [["Motor_Temp", "70000", "37000"]],
                [["Analog Input 3", "60000", "0"]],
                [["Analog Input 4", "60000", "0"]],
                [["48163", "39158", "33", "34"]],
            ],
            State.WARN,
            "[Motor_Temp]",
        ),
        (
            "1",
            [
                [["Tank_Level", "80000", "10000"]],
                [["Motor_Temp", "70000", "37000"]],
                [["Analog Input 3", "60000", "0"]],
                [["Analog Input 4", "60000", "0"]],
                [["48163", "39158", "33", "34"]],
            ],
            State.WARN,
            "[Tank_Level]",
        ),
    ],
)
def test_check_teracom_tcw241_analog(
    item: str,
    info: Sequence[StringTable],
    expected_state: State,
    expected_summary_contains: str,
) -> None:
    parsed = parse_tcw241_analog(info)
    results = list(check_tcw241_analog(item, parsed))
    result_objs = [r for r in results if isinstance(r, Result)]
    assert len(result_objs) == 1
    assert result_objs[0].state == expected_state
    assert expected_summary_contains in result_objs[0].summary
