#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="misc"


from typing import Any

import pytest

from cmk.ccc.version import Edition, edition
from cmk.gui.utils.ntop import (
    get_ntop_misconfiguration_reason,
    is_ntop_available,
    is_ntop_configured,
)
from cmk.utils import paths


@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
@pytest.mark.usefixtures("load_config")
def test_is_ntop_available() -> None:
    assert not is_ntop_available()


@pytest.mark.usefixtures("load_config")
@pytest.mark.parametrize(
    "ntop_connection, custom_user, answer, reason",
    [
        (
            {"is_activated": False},
            "",
            False,
            "ntopng integration is not activated in the global settings.",
        ),
        (
            {"is_activated": True, "use_custom_attribute_as_ntop_username": False},
            "",
            True,
            "",
        ),
        (
            {"is_activated": True, "use_custom_attribute_as_ntop_username": "ntop_alias"},
            "",
            False,
            (
                "The ntopng username should be derived from 'ntopng Username' "
                "under the current's user settings (identity) but this is not "
                "set for the current user."
            ),
        ),
        (
            {"is_activated": True, "use_custom_attribute_as_ntop_username": "ntop_alias"},
            "a_ntop_user",
            True,
            "",
        ),
    ],
)
@pytest.mark.skipif(
    edition(paths.omd_root) is not Edition.COMMUNITY,
    reason="Remove condition with CMK-32598",
)
def test_is_ntop_configured_and_reason(
    ntop_connection: dict[str, Any],
    custom_user: str,
    answer: bool,
    reason: str,
) -> None:
    assert not is_ntop_configured()
    assert get_ntop_misconfiguration_reason() == "ntopng integration is only available in CEE"
