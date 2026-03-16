#!/usr/bin/env python3
# Copyright (C) 2020 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.gui.graphing._artwork import (
    Curve,
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
from cmk.gui.graphing._time_series import TimeSeries


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
    rrd_data = TimeSeries(
        start=1,
        end=2,
        step=1,
        values=[],
    )
    assert list(
        _order_graph_curves_for_legend_and_mouse_hover(
            [
                Curve(
                    line_type="line",
                    color="",
                    title="1",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="ref",
                    color="",
                    title="2",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="-area",
                    color="",
                    title="3",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="stack",
                    color="",
                    title="4",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="area",
                    color="",
                    title="5",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="-stack",
                    color="",
                    title="6",
                    attributes={},
                    rrddata=rrd_data,
                ),
                Curve(
                    line_type="stack",
                    color="",
                    title="7",
                    attributes={},
                    rrddata=rrd_data,
                ),
            ]
        )
    ) == [
        Curve(
            color="",
            line_type="line",
            attributes={},
            rrddata=rrd_data,
            title="1",
        ),
        Curve(
            color="",
            line_type="stack",
            attributes={},
            rrddata=rrd_data,
            title="7",
        ),
        Curve(
            color="",
            line_type="area",
            attributes={},
            rrddata=rrd_data,
            title="5",
        ),
        Curve(
            color="",
            line_type="stack",
            attributes={},
            rrddata=rrd_data,
            title="4",
        ),
        Curve(
            color="",
            line_type="-area",
            attributes={},
            rrddata=rrd_data,
            title="3",
        ),
        Curve(
            color="",
            line_type="-stack",
            attributes={},
            rrddata=rrd_data,
            title="6",
        ),
        Curve(
            color="",
            line_type="ref",
            attributes={},
            rrddata=rrd_data,
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
