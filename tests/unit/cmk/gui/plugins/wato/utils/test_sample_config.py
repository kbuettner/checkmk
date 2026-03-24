#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

import cmk.gui.watolib.config_domain_name as utils
from cmk.ccc.version import Edition, edition
from cmk.utils import paths


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_registered_generators() -> None:
    expected_generators = [
        "acknowledge_initial_werks",
        "contact_groups",
        "basic_wato_config",
        "create_initial_admin_user",
        "create_local_site_connection",
        "create_registration_automation_user",
        "ec_sample_rule_pack",
    ]

    assert sorted(utils.sample_config_generator_registry.keys()) == sorted(expected_generators)


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_get_sorted_generators() -> None:
    expected = [
        "contact_groups",
        "basic_wato_config",
        "create_local_site_connection",
        "acknowledge_initial_werks",
        "ec_sample_rule_pack",
        "create_initial_admin_user",
        "create_registration_automation_user",
    ]

    assert {g.ident() for g in utils.sample_config_generator_registry.get_generators()} == set(
        expected
    )
