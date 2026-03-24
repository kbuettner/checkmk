#!/usr/bin/env python3
# Copyright (C) 2021 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.ccc.version import Edition, edition
from cmk.post_rename_site import main
from cmk.utils import paths


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_load_plugins() -> None:
    """The test changes a global variable `rename_action_registry`.
    We can't reliably monkey patch this variable - must use separate module for testing"""
    assert {p.name for p in main.load_plugins()} == {
        "sites",
        "messaging",
        "hosts_and_folders",
        "update_core_config",
        "warn_remote_site",
        "warn_about_network_ports",
        "warn_about_configs_to_review",
    }
