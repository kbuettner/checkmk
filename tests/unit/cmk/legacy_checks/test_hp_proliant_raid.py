#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="misc"
# mypy: disable-error-code="no-untyped-def"

from cmk.agent_based.v2 import render
from cmk.legacy_checks.hp_proliant_raid import (
    check_hp_proliant_raid,
    discover_hp_proliant_raid,
    parse_hp_proliant_raid,
)

STRING_TABLE = [
    ["1", "", "2", "286070", "4294967295"],
    ["2", "", "2", "25753986", "4294967295"],
    ["3", "", "2", "30523320", "4294967295"],
    ["4", "", "2", "15", "4294967295"],
    ["5", "", "2", "15", "4294967295"],
    ["6", "", "2", "17169273", "4294967295"],
]


def test_discover_hp_proliant_raid_no_snmp_data() -> None:
    assert not list(discover_hp_proliant_raid({}))


def test_discover_hp_proliant_raid_aa() -> None:
    discovery_results = list(discover_hp_proliant_raid(parse_hp_proliant_raid(STRING_TABLE)))
    assert discovery_results == [
        ("1", None),
        ("2", None),
        ("3", None),
        ("4", None),
        ("5", None),
        ("6", None),
    ]


def test_check_hp_proliant_raid_item_not_found() -> None:
    assert not list(check_hp_proliant_raid("!111elf", None, parse_hp_proliant_raid(STRING_TABLE)))


def test_check_hp_proliant_raid() -> None:
    assert list(check_hp_proliant_raid("1", None, parse_hp_proliant_raid(STRING_TABLE))) == [
        (0, "Status: OK"),
        (0, f"Logical volume size: {render.bytes(286070 * 1024 * 1024)}"),
    ]


def test_check_hp_proliant_raid_progress_cannot_be_determined() -> None:
    parsed = parse_hp_proliant_raid(
        [
            ["1", "banana", "7", "286070", "4294967295"],
        ]
    )
    assert list(check_hp_proliant_raid("banana 1", None, parsed)) == [
        (1, "Status: rebuilding"),
        (0, f"Logical volume size: {render.bytes(286070 * 1024 * 1024)}"),
        (0, "Rebuild: undetermined"),
    ]
