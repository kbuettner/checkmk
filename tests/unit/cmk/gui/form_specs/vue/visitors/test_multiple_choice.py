#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.form_specs.vue import DefaultValue as FormSpecDefaultValue
from cmk.gui.form_specs.vue import get_visitor, IncomingData, RawDiskData, RawFrontendData
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import DefaultValue, MultipleChoice, MultipleChoiceElement


@pytest.fixture(scope="module", name="multiple_choice_spec")
def spec() -> MultipleChoice:
    return MultipleChoice(
        elements=[
            MultipleChoiceElement(name="foo", title=Title("foo")),
            MultipleChoiceElement(name="bar", title=Title("bar")),
            MultipleChoiceElement(name="baz", title=Title("baz")),
        ],
        prefill=DefaultValue(["foo", "bar"]),
    )


SORTED_GOOD_CHOICES_FRONTEND = sorted(
    [{"name": "foo", "title": "foo"}, {"name": "bar", "title": "bar"}], key=lambda x: x["name"]
)
SORTED_GOOD_CHOICES_DISK = sorted(["foo", "bar"])


@pytest.mark.parametrize(
    "sorted_good_choices",
    [
        RawDiskData(SORTED_GOOD_CHOICES_DISK),
        RawFrontendData(SORTED_GOOD_CHOICES_FRONTEND),
    ],
)
def test_multiple_choice(
    # request_context: None,
    # patch_theme: None,
    # with_user: tuple[UserId, str],
    sorted_good_choices: IncomingData,
    multiple_choice_spec: MultipleChoice,
) -> None:
    # Note: custom sorting will be implemented with MultipleChoiceExpanded
    visitor = get_visitor(multiple_choice_spec)
    _vue_spec, vue_value = visitor.to_vue(sorted_good_choices)
    # Send good choice to vue
    assert vue_value == SORTED_GOOD_CHOICES_FRONTEND

    # No validation problems
    validation_messages = visitor.validate(sorted_good_choices)
    assert len(validation_messages) == 0

    # Write choice back to disk
    assert visitor.to_disk(sorted_good_choices) == SORTED_GOOD_CHOICES_DISK


SOME_BAD_CHOICE_FRONTEND = [
    {"name": "foo", "title": "foo"},
    {"name": "bar", "title": "bar"},
    {"name": "unknown_value", "title": "unknown_value"},
]
SOME_BAD_CHOICE_DISK = ["foo", "bar", "unknown_value"]
SORTED_SOME_BAD_CHOICE_FILTERED_FRONTEND = sorted(
    [{"name": "foo", "title": "foo"}, {"name": "bar", "title": "bar"}], key=lambda x: x["name"]
)
SORTED_SOME_BAD_CHOICE_FILTERED_DISK = sorted(["foo", "bar"])


@pytest.mark.parametrize(
    "some_bad_choice",
    [RawDiskData(SOME_BAD_CHOICE_DISK), RawFrontendData(SOME_BAD_CHOICE_FRONTEND)],
)
def test_multiple_choice_with_invalid_key(
    some_bad_choice: IncomingData,
    multiple_choice_spec: MultipleChoice,
) -> None:
    # Note: custom sorting will be implemented with MultipleChoiceExpanded
    # Check behaviour: Invalid keys are filtered out during parsing
    visitor = get_visitor(multiple_choice_spec)
    _vue_spec, vue_value = visitor.to_vue(some_bad_choice)
    # Send good choice to vue
    assert vue_value == SORTED_SOME_BAD_CHOICE_FILTERED_FRONTEND

    # No validation problems
    validation_messages = visitor.validate(some_bad_choice)
    assert len(validation_messages) == 0

    # Write choice back to disk
    assert visitor.to_disk(some_bad_choice) == SORTED_SOME_BAD_CHOICE_FILTERED_DISK


def test_parse_default_value(multiple_choice_spec: MultipleChoice) -> None:
    visitor = get_visitor(multiple_choice_spec)
    assert visitor._parse_value(FormSpecDefaultValue()) == SORTED_GOOD_CHOICES_FRONTEND
