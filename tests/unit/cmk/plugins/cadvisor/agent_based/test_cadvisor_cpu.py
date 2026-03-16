#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping, Sequence

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State, StringTable
from cmk.plugins.cadvisor.agent_based.cadvisor_cpu import (
    check_cadvisor_cpu,
    discover_cadvisor_cpu,
    parse_cadvisor_cpu,
)


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        (
            [
                [
                    '{"cpu_user": [{"value": "0.10996819381471273", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}], "cpu_system": [{"value": "0.12688637747851422", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}]}'
                ]
            ],
            [Service()],
        ),
    ],
)
def test_discover_cadvisor_cpu(
    string_table: StringTable, expected_discoveries: Sequence[Service]
) -> None:
    """Test discovery function for cadvisor_cpu check."""
    parsed = parse_cadvisor_cpu(string_table)
    result = list(discover_cadvisor_cpu(parsed))
    assert result == expected_discoveries


@pytest.mark.parametrize(
    "params, string_table, expected_results",
    [
        (
            {},
            [
                [
                    '{"cpu_user": [{"value": "0.10996819381471273", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}], "cpu_system": [{"value": "0.12688637747851422", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}]}'
                ]
            ],
            [
                Result(state=State.OK, summary="User: 0.11%"),
                Metric("user", 0.10996819381471273),
                Result(state=State.OK, summary="System: 0.13%"),
                Metric("system", 0.12688637747851422),
                Result(state=State.OK, summary="Total CPU: 0.24%"),
                Metric("util", 0.23685457129322696),
            ],
        ),
    ],
)
def test_check_cadvisor_cpu(
    params: Mapping[str, object],
    string_table: StringTable,
    expected_results: Sequence[Result | Metric],
) -> None:
    """Test check function for cadvisor_cpu check."""
    parsed = parse_cadvisor_cpu(string_table)
    result = list(check_cadvisor_cpu(params, parsed))
    assert result == expected_results
