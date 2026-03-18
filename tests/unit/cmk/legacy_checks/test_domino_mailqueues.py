#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Metric, Result, State, StringTable
from cmk.legacy_checks.domino_mailqueues import (
    check_domino_mailqueues,
    discover_domino_mailqueues,
    DominoMailqueuesParams,
    parse_domino_mailqueues,
)


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        (
            [["1", "4711", "815", "1", "12"]],
            [
                "lnDeadMail",
                "lnWaitingMail",
                "lnMailHold",
                "lnMailTotalPending",
                "InMailWaitingforDNS",
            ],
        ),
    ],
)
def test_discover_domino_mailqueues(
    string_table: StringTable, expected_discoveries: Sequence[str]
) -> None:
    parsed = parse_domino_mailqueues(string_table)
    result = sorted(s.item or "" for s in discover_domino_mailqueues(parsed))
    assert result == sorted(expected_discoveries)


@pytest.mark.parametrize(
    "item, params, string_table, expected_state, expected_summary_substring",
    [
        (
            "lnDeadMail",
            {"queue_length": (300, 350)},
            [["1", "4711", "815", "1", "12"]],
            State.OK,
            "Dead mails",
        ),
        (
            "lnWaitingMail",
            {"queue_length": (300, 350)},
            [["1", "4711", "815", "1", "12"]],
            State.CRIT,
            "Waiting mails",
        ),
        (
            "lnMailHold",
            {"queue_length": (300, 350)},
            [["1", "4711", "815", "1", "12"]],
            State.CRIT,
            "Mails on hold",
        ),
        (
            "lnMailTotalPending",
            {"queue_length": (300, 350)},
            [["1", "4711", "815", "1", "12"]],
            State.OK,
            "Total pending mails",
        ),
        (
            "InMailWaitingforDNS",
            {"queue_length": (300, 350)},
            [["1", "4711", "815", "1", "12"]],
            State.OK,
            "Mails waiting for DNS",
        ),
    ],
)
def test_check_domino_mailqueues(
    item: str,
    params: DominoMailqueuesParams,
    string_table: StringTable,
    expected_state: State,
    expected_summary_substring: str,
) -> None:
    parsed = parse_domino_mailqueues(string_table)
    results = list(check_domino_mailqueues(item, params, parsed))
    result_objs = [r for r in results if isinstance(r, Result)]
    metric_objs = [r for r in results if isinstance(r, Metric)]
    assert len(result_objs) == 1
    assert result_objs[0].state == expected_state
    assert expected_summary_substring in result_objs[0].summary
    assert len(metric_objs) == 1
    assert metric_objs[0].name == "mails"
