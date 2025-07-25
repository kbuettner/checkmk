#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import Any

from cmk.ccc.exceptions import MKGeneralException
from cmk.gui.form_specs.private import SingleChoiceElementExtended, SingleChoiceExtended
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import FormSpec, ServiceState


def recompose(form_spec: FormSpec[Any]) -> FormSpec[Any]:
    if not isinstance(form_spec, ServiceState):
        raise MKGeneralException(
            f"Cannot recompose form spec. Expected a ServiceState form spec, got {type(form_spec)}"
        )

    return SingleChoiceExtended(
        # FormSpec:
        title=form_spec.title,
        help_text=form_spec.help_text,
        migrate=form_spec.migrate,
        custom_validate=form_spec.custom_validate,
        # SingleChoice
        elements=[
            SingleChoiceElementExtended(
                name=ServiceState.OK,
                title=Title("OK"),
            ),
            SingleChoiceElementExtended(
                name=ServiceState.WARN,
                title=Title("WARN"),
            ),
            SingleChoiceElementExtended(
                name=ServiceState.CRIT,
                title=Title("CRIT"),
            ),
            SingleChoiceElementExtended(
                name=ServiceState.UNKNOWN,
                title=Title("UNKNOWN"),
            ),
        ],
        prefill=form_spec.prefill,
    )
