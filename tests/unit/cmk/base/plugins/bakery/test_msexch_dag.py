#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin
from cmk.base.plugins.bakery.msexch_dag import get_msexch_files


def test_msexch_dag_files() -> None:
    result = list(get_msexch_files(None))
    expected = [
        Plugin(base_os=OS.WINDOWS, source=Path("msexch_dag.ps1")),
    ]
    assert result == expected
