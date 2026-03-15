#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.bakery.v1 import WindowsGlobalConfigEntry
from cmk.base.plugins.bakery.win_agent_disabled_sections import (
    get_win_agent_disabled_sections_windows_config,
)


def test_win_agent_disabled_sections_windows_config() -> None:
    conf = "check_mk logwatch"
    result = list(get_win_agent_disabled_sections_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="disabled_sections", content="check_mk logwatch"),
    ]


def test_win_agent_disabled_sections_windows_config_empty() -> None:
    conf = ""
    result = list(get_win_agent_disabled_sections_windows_config(conf))
    assert result == [
        WindowsGlobalConfigEntry(name="disabled_sections", content=""),
    ]
