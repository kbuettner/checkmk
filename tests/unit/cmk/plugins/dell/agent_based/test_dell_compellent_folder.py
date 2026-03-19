#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.agent_based.v2 import Service
from cmk.plugins.dell.agent_based.dell_compellent_folder import (
    discover_dell_compellent_folder,
    parse_dell_compellent_folder,
)


def test_discover_dell_compellent_folder() -> None:
    section = parse_dell_compellent_folder([["", "", ""], ["2", "237273", "130456"]])
    assert list(discover_dell_compellent_folder(section)) == [Service(item="2")]
