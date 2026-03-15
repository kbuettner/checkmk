#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.bakery.v1 import OS, Plugin, PluginConfig
from cmk.base.plugins.bakery.mk_podman import get_mk_podman_files


def test_mk_podman_files_auto_detection() -> None:
    conf = {
        "deploy": True,
        "socket_detection": ("auto", None),
        "piggyback_name_method": "nodename_name",
    }
    result = sorted(get_mk_podman_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_podman.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=[
                    "[PODMAN]",
                    "socket_detection_method: auto",
                    "piggyback_name_method: nodename_name",
                ],
                target=Path("mk_podman.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_podman_files_manual_sockets() -> None:
    conf = {
        "deploy": True,
        "socket_detection": ("manual", ["/run/podman/podman.sock", "/tmp/podman.sock"]),
        "piggyback_name_method": "name",
    }
    result = sorted(get_mk_podman_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_podman.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=[
                    "[PODMAN]",
                    "socket_detection_method: manual",
                    "socket_paths: /run/podman/podman.sock,/tmp/podman.sock",
                    "piggyback_name_method: name",
                ],
                target=Path("mk_podman.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_podman_files_not_deployed() -> None:
    conf = {
        "deploy": False,
        "socket_detection": ("auto", None),
    }
    result = list(get_mk_podman_files(conf))
    assert result == []


def test_mk_podman_files_only_root_socket() -> None:
    conf = {
        "deploy": True,
        "socket_detection": ("only_root_socket", None),
        "piggyback_name_method": "name_id",
    }
    result = sorted(get_mk_podman_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_podman.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=[
                    "[PODMAN]",
                    "socket_detection_method: only_root_socket",
                    "piggyback_name_method: name_id",
                ],
                target=Path("mk_podman.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected


def test_mk_podman_files_only_user_sockets() -> None:
    conf = {
        "deploy": True,
        "socket_detection": ("only_user_sockets", None),
    }
    result = sorted(get_mk_podman_files(conf), key=repr)
    expected = sorted(
        [
            Plugin(base_os=OS.LINUX, source=Path("mk_podman.py")),
            PluginConfig(
                base_os=OS.LINUX,
                lines=[
                    "[PODMAN]",
                    "socket_detection_method: only_user_sockets",
                    "piggyback_name_method: nodename_name",
                ],
                target=Path("mk_podman.cfg"),
                include_header=True,
            ),
        ],
        key=repr,
    )
    assert result == expected
