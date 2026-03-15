#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path
from unittest.mock import patch

import pytest

from cmk.bakery.v1 import OS, Plugin, PluginConfig
from cmk.base.plugins.bakery.mk_tsm import get_mk_tsm_files, TSMConfig


def test_mk_tsm_files_sync_explicit_password() -> None:
    conf: TSMConfig = {
        "deployment": ("sync", None),
        "auth": {
            "user": "admin",
            "password": ("cmk_postprocessed", "explicit_password", ("uuid1", "mysecret")),
        },
    }
    result = sorted(get_mk_tsm_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_tsm"), interval=None),
            PluginConfig(
                base_os=OS.LINUX,
                lines=["# Credentials for dsmadmc:", "TSM_USER=admin", "TSM_PASSWORD=mysecret"],
                target=Path("tsm.cfg"),
                include_header=True,
            ),
            Plugin(base_os=OS.AIX, source=Path("mk_tsm"), interval=None),
            PluginConfig(
                base_os=OS.AIX,
                lines=["# Credentials for dsmadmc:", "TSM_USER=admin", "TSM_PASSWORD=mysecret"],
                target=Path("tsm.cfg"),
                include_header=True,
            ),
            Plugin(base_os=OS.SOLARIS, source=Path("mk_tsm"), interval=None),
            PluginConfig(
                base_os=OS.SOLARIS,
                lines=["# Credentials for dsmadmc:", "TSM_USER=admin", "TSM_PASSWORD=mysecret"],
                target=Path("tsm.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_tsm_files_cached() -> None:
    conf: TSMConfig = {
        "deployment": ("cached", 300.0),
        "auth": {
            "user": "tsm_user",
            "password": ("cmk_postprocessed", "explicit_password", ("uuid2", "pass123")),
        },
    }
    result = sorted(get_mk_tsm_files(conf), key=repr)
    # All plugins should have interval=300
    plugins = [r for r in result if isinstance(r, Plugin)]
    assert len(plugins) == 3
    for plugin in plugins:
        assert plugin.interval == 300


def test_mk_tsm_files_do_not_deploy() -> None:
    conf: TSMConfig = {
        "deployment": ("do_not_deploy", None),
        "auth": {
            "user": "admin",
            "password": ("cmk_postprocessed", "explicit_password", ("uuid1", "mysecret")),
        },
    }
    result = list(get_mk_tsm_files(conf))
    assert result == []


def test_mk_tsm_files_stored_password() -> None:
    conf: TSMConfig = {
        "deployment": ("sync", None),
        "auth": {
            "user": "admin",
            "password": ("cmk_postprocessed", "stored_password", ("pw_id_1", "")),
        },
    }
    with patch("cmk.base.plugins.bakery.mk_tsm.lookup_for_bakery", return_value="looked_up_secret"):
        result = sorted(get_mk_tsm_files(conf), key=repr)
    plugins_config = [r for r in result if isinstance(r, PluginConfig)]
    assert len(plugins_config) == 3
    for pc in plugins_config:
        assert "TSM_PASSWORD=looked_up_secret" in pc.lines


def test_mk_tsm_files_missing_auth() -> None:
    conf: TSMConfig = {
        "deployment": ("sync", None),
    }
    with pytest.raises(ValueError, match="Missing 'auth' configuration"):
        list(get_mk_tsm_files(conf))


def test_mk_tsm_files_default_deployment() -> None:
    """When no deployment is set, defaults to do_not_deploy."""
    conf: TSMConfig = {
        "auth": {
            "user": "admin",
            "password": ("cmk_postprocessed", "explicit_password", ("uuid1", "secret")),
        },
    }
    result = list(get_mk_tsm_files(conf))
    assert result == []


def test_mk_tsm_files_all_os_covered() -> None:
    conf: TSMConfig = {
        "deployment": ("sync", None),
        "auth": {
            "user": "admin",
            "password": ("cmk_postprocessed", "explicit_password", ("uuid1", "secret")),
        },
    }
    result = list(get_mk_tsm_files(conf))
    plugins = [r for r in result if isinstance(r, Plugin)]
    os_set = {p.base_os for p in plugins}
    assert os_set == {OS.LINUX, OS.AIX, OS.SOLARIS}
