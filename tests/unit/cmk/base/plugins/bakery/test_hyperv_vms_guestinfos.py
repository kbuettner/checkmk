#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin
from cmk.base.plugins.bakery.hyperv_vms_guestinfos import get_hyperv_vms_guestinfos_files


def test_hyperv_vms_guestinfos_files_enabled() -> None:
    result = list(get_hyperv_vms_guestinfos_files(True))
    expected = [Plugin(base_os=OS.WINDOWS, source=Path("hyperv_vms_guestinfos.ps1"))]
    assert result == expected


def test_hyperv_vms_guestinfos_files_disabled() -> None:
    result = list(get_hyperv_vms_guestinfos_files(False))
    assert result == []


def test_hyperv_vms_guestinfos_files_none() -> None:
    result = list(get_hyperv_vms_guestinfos_files(None))
    assert result == []
