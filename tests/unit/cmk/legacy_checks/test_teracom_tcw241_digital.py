#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.legacy_checks.teracom_tcw241_digital import (
    check_tcw241_digital,
    discover_teracom_tcw241_digital,
    parse_tcw241_digital,
)


@pytest.mark.parametrize(
    "info, expected_discoveries",
    [
        (
            [
                [["Tank_Status", "NEA_Status", "Digital Input 3", "Digital Input 4"]],
                [["1", "1", "1", "1"]],
            ],
            [
                Service(item="1"),
                Service(item="2"),
                Service(item="3"),
                Service(item="4"),
            ],
        ),
    ],
)
def test_discover_teracom_tcw241_digital(
    info: Sequence[StringTable], expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_tcw241_digital(info)
    result = list(discover_teracom_tcw241_digital(parsed))
    assert sorted(result, key=lambda s: s.item or "") == sorted(
        expected_discoveries, key=lambda s: s.item or ""
    )


@pytest.mark.parametrize(
    "item, info, expected_results",
    [
        (
            "4",
            [
                [["Tank_Status", "NEA_Status", "Digital Input 3", "Digital Input 4"]],
                [["1", "1", "1", "1"]],
            ],
            [Result(state=State.OK, summary="[Digital Input 4] is open")],
        ),
        (
            "3",
            [
                [["Tank_Status", "NEA_Status", "Digital Input 3", "Digital Input 4"]],
                [["1", "1", "1", "1"]],
            ],
            [Result(state=State.OK, summary="[Digital Input 3] is open")],
        ),
        (
            "2",
            [
                [["Tank_Status", "NEA_Status", "Digital Input 3", "Digital Input 4"]],
                [["1", "1", "1", "1"]],
            ],
            [Result(state=State.OK, summary="[NEA_Status] is open")],
        ),
        (
            "1",
            [
                [["Tank_Status", "NEA_Status", "Digital Input 3", "Digital Input 4"]],
                [["1", "1", "1", "1"]],
            ],
            [Result(state=State.OK, summary="[Tank_Status] is open")],
        ),
    ],
)
def test_check_teracom_tcw241_digital(
    item: str, info: Sequence[StringTable], expected_results: Sequence[Result]
) -> None:
    parsed = parse_tcw241_digital(info)
    result = list(check_tcw241_digital(item, parsed))
    assert result == expected_results
