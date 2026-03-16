#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.legacy_checks.sansymphony_virtualdiskstatus import (
    check_sansymphony_virtualdiskstatus,
    discover_sansymphony_virtualdiskstatus,
    parse_sansymphony_virtualdiskstatus,
)


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        (
            [["testvmfs01", "Online"], ["vmfs01", "anything", "else"]],
            [Service(item="testvmfs01"), Service(item="vmfs01")],
        ),
    ],
)
def test_discover_sansymphony_virtualdiskstatus(
    string_table: StringTable, expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_sansymphony_virtualdiskstatus(string_table)
    result = list(discover_sansymphony_virtualdiskstatus(parsed))
    assert sorted(result, key=lambda s: s.item or "") == sorted(
        expected_discoveries, key=lambda s: s.item or ""
    )


@pytest.mark.parametrize(
    "item, string_table, expected_state, expected_summary",
    [
        (
            "testvmfs01",
            [["testvmfs01", "Online"], ["vmfs01", "anything", "else"]],
            State.OK,
            "Volume state is: Online",
        ),
        (
            "vmfs01",
            [["testvmfs01", "Online"], ["vmfs01", "anything", "else"]],
            State.CRIT,
            "Volume state is: anything else",
        ),
    ],
)
def test_check_sansymphony_virtualdiskstatus(
    item: str, string_table: StringTable, expected_state: State, expected_summary: str
) -> None:
    parsed = parse_sansymphony_virtualdiskstatus(string_table)
    results = list(check_sansymphony_virtualdiskstatus(item, parsed))
    result_objs = [r for r in results if isinstance(r, Result)]
    assert result_objs[0].state == expected_state
    assert result_objs[0].summary == expected_summary
