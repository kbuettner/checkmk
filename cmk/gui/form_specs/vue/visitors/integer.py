#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from typing import Any, Callable, Sequence

from cmk.gui.form_specs.private.validators import IsInteger
from cmk.gui.form_specs.vue.autogen_type_defs import vue_formspec_components as VueComponents
from cmk.gui.form_specs.vue.registries import FormSpecVisitor
from cmk.gui.form_specs.vue.type_defs import (
    DataForDisk,
    DataOrigin,
    DEFAULT_VALUE,
    Value,
    VisitorOptions,
)
from cmk.gui.form_specs.vue.utils import compute_validation_errors, get_title_and_help, localize
from cmk.gui.form_specs.vue.validators import build_vue_validators

from cmk.rulesets.v1.form_specs import Integer


class IntegerVisitor(FormSpecVisitor):
    def __init__(self, form_spec: Integer, options: VisitorOptions) -> None:
        self.form_spec = form_spec
        self.options = options

    def parse_value(self, value: Any) -> int:
        if self.options.data_origin == DataOrigin.DISK and self.form_spec.migrate:
            value = self.form_spec.migrate(value)

        if isinstance(value, DEFAULT_VALUE):
            value = self.form_spec.prefill.value

        if not isinstance(value, int):
            raise TypeError(f"Expected a integer, got {type(value)}")

        return value

    def _validators(self) -> Sequence[Callable[[int], object]]:
        return [IsInteger()] + (
            list(self.form_spec.custom_validate) if self.form_spec.custom_validate else []
        )

    def to_vue(self, value: int) -> tuple[VueComponents.FormSpec, Value]:
        title, help_text = get_title_and_help(self.form_spec)
        return (
            VueComponents.Integer(
                title=title,
                help=help_text,
                label=localize(self.form_spec.label),
                validators=build_vue_validators(self._validators()),
            ),
            value,
        )

    def validate(self, value: int) -> list[VueComponents.ValidationMessage]:
        return compute_validation_errors(self._validators(), value)

    def to_disk(self, value: int) -> DataForDisk:
        return value
