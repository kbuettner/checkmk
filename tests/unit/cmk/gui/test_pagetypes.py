#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.ccc.version import Edition, edition
from cmk.gui.pagetypes import PagetypeTopics
from cmk.gui.utils.script_helpers import application_and_request_context
from cmk.utils import paths


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_registered_pagetype_topics() -> None:
    expected = [
        "analyze",
        "applications",
        "bi",
        "cloud",
        "events",
        "history",
        "inventory",
        "it_efficiency",
        "monitoring",
        "my_workplace",
        "other",
        "overview",
        "problems",
        "synthetic_monitoring",
    ]

    with application_and_request_context():
        assert sorted(list(PagetypeTopics.builtin_pages().keys())) == sorted(expected)
