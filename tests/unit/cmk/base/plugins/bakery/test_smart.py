#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin
from cmk.base.plugins.bakery.smart import get_smart_files


def test_smart_files_smart_posix() -> None:
    result = list(get_smart_files("smart_posix"))
    expected = [
        Plugin(base_os=OS.LINUX, source=Path("smart_posix")),
    ]
    assert result == expected


def test_smart_files_smart() -> None:
    result = list(get_smart_files("smart"))
    expected = [
        Plugin(base_os=OS.LINUX, source=Path("smart")),
    ]
    assert result == expected
