#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path
from pprint import pformat

from cmk.bakery.v1 import OS, Plugin, PluginConfig
from cmk.base.plugins.bakery.nginx_status import get_nginx_status_files


def test_nginx_status_files_static() -> None:
    servers = [("myhost", 80)]
    conf = ("static", servers)
    result = sorted(get_nginx_status_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("nginx_status.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=["servers = %s" % pformat(servers)],
                target=Path("nginx_status.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_nginx_status_files_auto() -> None:
    ssl_ports = [443, 8443]
    conf = ("auto", ssl_ports)
    result = sorted(get_nginx_status_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("nginx_status.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=["ssl_ports = %r" % ssl_ports],
                target=Path("nginx_status.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected
