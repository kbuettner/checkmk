#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin
from cmk.base.plugins.bakery.veeam_backup_status import get_veeam_backup_status_files


def test_veeam_backup_status_files() -> None:
    result = list(get_veeam_backup_status_files(None))
    expected = [
        Plugin(base_os=OS.WINDOWS, source=Path("veeam_backup_status.ps1")),
    ]
    assert result == expected
