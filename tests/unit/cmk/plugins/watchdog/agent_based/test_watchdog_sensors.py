#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.plugins.watchdog.agent_based.watchdog_sensors import (
    check_watchdog_sensors,
    discover_watchdog_sensors,
    parse_watchdog_sensors,
)


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        (
            [
                [["3.2.0", "1"]],
                [
                    ["1", "First Floor Ambient", "1", "213", "37", "60", ""],
                    ["2", "Second Floor Ambient", "1", "200", "30", "40", ""],
                ],
            ],
            [Service(item="Watchdog 1"), Service(item="Watchdog 2")],
        ),
    ],
)
def test_discover_watchdog_sensors(
    string_table: Sequence[StringTable], expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_watchdog_sensors(string_table)
    result = list(discover_watchdog_sensors(parsed))
    assert sorted(result, key=lambda s: s.item or "") == sorted(
        expected_discoveries, key=lambda s: s.item or ""
    )


@pytest.mark.parametrize(
    "item, string_table, expected_results",
    [
        (
            "Watchdog 1",
            [
                [["3.2.0", "1"]],
                [
                    ["1", "First Floor Ambient", "1", "213", "37", "60", ""],
                    ["2", "Second Floor Ambient", "1", "200", "30", "40", ""],
                ],
            ],
            [
                Result(state=State.OK, summary="available"),
                Result(state=State.OK, summary="Location: First Floor Ambient"),
            ],
        ),
        (
            "Watchdog 2",
            [
                [["3.2.0", "1"]],
                [
                    ["1", "First Floor Ambient", "1", "213", "37", "60", ""],
                    ["2", "Second Floor Ambient", "1", "200", "30", "40", ""],
                ],
            ],
            [
                Result(state=State.OK, summary="available"),
                Result(state=State.OK, summary="Location: Second Floor Ambient"),
            ],
        ),
    ],
)
def test_check_watchdog_sensors(
    item: str, string_table: Sequence[StringTable], expected_results: Sequence[Result]
) -> None:
    parsed = parse_watchdog_sensors(string_table)
    result = list(check_watchdog_sensors(item, parsed))
    assert result == expected_results
