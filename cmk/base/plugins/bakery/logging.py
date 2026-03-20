#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator, Mapping
from typing import Final

from .bakery_api.v1 import register, WindowsConfigEntry

_TO_YAML: Final = {
    "logging_level": "debug",
    "max_log_file_count": "max_file_count",
    "max_log_file_size": "max_file_size",
    "log_to_windbg": "windbg",
}


def get_logging_windows_config(
    conf: Mapping[str, str | int | bool],
) -> Iterator[WindowsConfigEntry]:
    yield from (
        WindowsConfigEntry(path=["global", "logging", _TO_YAML[key]], content=value)
        for key, value in conf.items()
    )


register.bakery_plugin(
    name="logging",
    windows_config_function=get_logging_windows_config,
)
