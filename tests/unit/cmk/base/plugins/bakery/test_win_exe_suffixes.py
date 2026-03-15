#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.bakery.v1 import WindowsGlobalConfigEntry
from cmk.base.plugins.bakery.win_exe_suffixes import (
    get_win_exe_suffixes_windows_config,
)


def test_win_exe_suffixes_windows_config() -> None:
    conf = "exe bat vbs"
    result = list(get_win_exe_suffixes_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="execute", content="exe bat vbs"),
    ]


def test_win_exe_suffixes_windows_config_single() -> None:
    conf = "ps1"
    result = list(get_win_exe_suffixes_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="execute", content="ps1"),
    ]
