#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin
from cmk.base.plugins.bakery.mk_zypper import get_mk_zypper_files


def test_mk_zypper_files() -> None:
    result = list(get_mk_zypper_files(300))
    expected = [
        Plugin(base_os=OS.LINUX, source=Path("mk_zypper"), interval=300),
    ]
    assert result == expected
