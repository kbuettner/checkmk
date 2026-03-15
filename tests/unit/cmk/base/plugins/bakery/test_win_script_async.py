#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.bakery.v1 import WindowsGlobalConfigEntry
from cmk.base.plugins.bakery.win_script_async import (
    get_win_script_async_windows_config,
)


def test_win_script_async_windows_config_parallel() -> None:
    conf = "parallel"
    result = list(get_win_script_async_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="async_script_execution", content="parallel"),
    ]


def test_win_script_async_windows_config_sequential() -> None:
    conf = "sequential"
    result = list(get_win_script_async_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="async_script_execution", content="sequential"),
    ]
