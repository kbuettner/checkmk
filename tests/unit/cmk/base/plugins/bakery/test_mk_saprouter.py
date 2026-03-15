#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin, PluginConfig
from cmk.base.plugins.bakery.mk_saprouter import get_mk_saprouter_files


def test_mk_saprouter_files() -> None:
    conf = {"user": "saprouter", "path": "/usr/sap/sapgenpse", "interval": 300}
    result = sorted(get_mk_saprouter_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_saprouter"), interval=300),
            PluginConfig(
                base_os=OS.LINUX,
                lines=["SAPROUTER_USER=saprouter", "SAPGENPSE_PATH=/usr/sap/sapgenpse"],
                target=Path("saprouter.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_saprouter_files_no_interval() -> None:
    conf = {"user": "admin", "path": "/opt/sapgenpse"}
    result = sorted(get_mk_saprouter_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_saprouter"), interval=None),
            PluginConfig(
                base_os=OS.LINUX,
                lines=["SAPROUTER_USER=admin", "SAPGENPSE_PATH=/opt/sapgenpse"],
                target=Path("saprouter.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_saprouter_files_special_chars() -> None:
    """Test that shell quoting is applied to user and path."""
    conf = {"user": "sap user", "path": "/path with spaces/sapgenpse"}
    result = sorted(get_mk_saprouter_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_saprouter"), interval=None),
            PluginConfig(
                base_os=OS.LINUX,
                lines=[
                    "SAPROUTER_USER='sap user'",
                    "SAPGENPSE_PATH='/path with spaces/sapgenpse'",
                ],
                target=Path("saprouter.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected
