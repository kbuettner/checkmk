#!/usr/bin/env python3
# Copyright (C) 2020 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.gui.graphing._artwork import (
    CurveValue,
    LayoutedCurve,
    LayoutedCurveArea,
    LayoutedCurveLine,
    LayoutedCurveStack,
    Scalars,
)
from cmk.gui.graphing._html_render import (
    _order_graph_curves_for_legend_and_mouse_hover,
    _render_title_elements_plain,
)


@pytest.mark.parametrize(
    "elements, result",
    [
        (
            ["first", "second"],
            "first / second",
        ),
        (
            ["", "second"],
            "second",
        ),
    ],
)
def test_render_title_elements_plain(elements: Sequence[str], result: str) -> None:
    assert _render_title_elements_plain(elements) == result


def test__order_graph_curves_for_legend_and_mouse_hover_curves() -> None:
    rendered_value = (123.456, "123.456")
    assert list(
        _order_graph_curves_for_legend_and_mouse_hover(
            [
                CurveValue(
                    line_type="line",
                    color="",
                    title="1",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="ref",
                    color="",
                    title="2",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="-area",
                    color="",
                    title="3",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="stack",
                    color="",
                    title="4",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="area",
                    color="",
                    title="5",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="-stack",
                    color="",
                    title="6",
                    rendered_value=rendered_value,
                ),
                CurveValue(
                    line_type="stack",
                    color="",
                    title="7",
                    rendered_value=rendered_value,
                ),
            ]
        )
    ) == [
        CurveValue(
            color="",
            line_type="line",
            rendered_value=rendered_value,
            title="1",
        ),
        CurveValue(
            color="",
            line_type="stack",
            rendered_value=rendered_value,
            title="7",
        ),
        CurveValue(
            color="",
            line_type="area",
            rendered_value=rendered_value,
            title="5",
        ),
        CurveValue(
            color="",
            line_type="stack",
            rendered_value=rendered_value,
            title="4",
        ),
        CurveValue(
            color="",
            line_type="-area",
            rendered_value=rendered_value,
            title="3",
        ),
        CurveValue(
            color="",
            line_type="-stack",
            rendered_value=rendered_value,
            title="6",
        ),
        CurveValue(
            color="",
            line_type="ref",
            rendered_value=rendered_value,
            title="2",
        ),
    ]


@pytest.mark.parametrize(
    "curves, result",
    [
        pytest.param(
            [
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="1",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="2",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveLine(
                    line_type="line",
                    color="",
                    title="3",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
            ],
            [
                LayoutedCurveLine(
                    line_type="line",
                    color="",
                    title="3",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="2",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="1",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
            ],
            id="stack-and-line",
        ),
        pytest.param(
            [
                LayoutedCurveStack(
                    line_type="-stack",
                    color="",
                    title="1",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveArea(
                    line_type="-area",
                    color="",
                    title="2",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveLine(
                    line_type="-line",
                    color="",
                    title="3",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="4",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveArea(
                    line_type="area",
                    color="",
                    title="5",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveLine(
                    line_type="line",
                    color="",
                    title="6",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
            ],
            [
                LayoutedCurveLine(
                    line_type="line",
                    color="",
                    title="6",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveArea(
                    line_type="area",
                    color="",
                    title="5",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="stack",
                    color="",
                    title="4",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveStack(
                    line_type="-stack",
                    color="",
                    title="1",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveArea(
                    line_type="-area",
                    color="",
                    title="2",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
                LayoutedCurveLine(
                    line_type="-line",
                    color="",
                    title="3",
                    scalars=Scalars(
                        pin=(None, "n/a"),
                        first=(None, "n/a"),
                        last=(None, "n/a"),
                        max=(None, "n/a"),
                        min=(None, "n/a"),
                        average=(None, "n/a"),
                    ),
                    attributes={},
                    points=[],
                ),
            ],
            id="lower-and-upper",
        ),
    ],
)
def test__order_graph_curves_for_legend_and_mouse_hover_layouted_curves(
    curves: Sequence[LayoutedCurve], result: Sequence[LayoutedCurve]
) -> None:
    assert list(_order_graph_curves_for_legend_and_mouse_hover(curves)) == result
