#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.ccc.version import Edition, edition
from cmk.gui.watolib.timeperiods import timeperiod_usage_finder_registry
from cmk.utils import paths


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_group_usage_finder_registry_entries() -> None:
    expected = [
        "find_timeperiod_usage_in_ec_rules",
        "find_timeperiod_usage_in_host_and_service_rules",
        "find_timeperiod_usage_in_notification_rules",
        "find_timeperiod_usage_in_time_specific_parameters",
        "find_timeperiod_usage_in_users",
    ]

    registered = [f.__name__ for f in timeperiod_usage_finder_registry.values()]
    assert sorted(registered) == sorted(expected)
