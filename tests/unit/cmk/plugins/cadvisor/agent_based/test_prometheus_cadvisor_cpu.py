#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# NOTE: This file has been created by an LLM (from something that was worse).
# It mostly serves as test to ensure we don't accidentally break anything.
# If you encounter something weird in here, do not hesitate to replace this
# test by something more appropriate.

from collections.abc import Mapping

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State
from cmk.plugins.cadvisor.agent_based.cadvisor_cpu import (
    check_cadvisor_cpu,
    discover_cadvisor_cpu,
    parse_cadvisor_cpu,
)


@pytest.fixture
def parsed() -> Mapping[str, float]:
    """Create parsed cAdvisor CPU data using actual parse function."""
    string_table = [
        [
            '{"cpu_user": [{"value": "0.10996819381471273", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}], "cpu_system": [{"value": "0.12688637747851422", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}]}'
        ]
    ]
    return parse_cadvisor_cpu(string_table)


def test_cadvisor_cpu_discovery(parsed: Mapping[str, float]) -> None:
    result = list(discover_cadvisor_cpu(parsed))
    assert len(result) == 1
    assert result[0] == Service()


def test_cadvisor_cpu_check(parsed: Mapping[str, float]) -> None:
    results = list(check_cadvisor_cpu(params={}, section=parsed))

    result_objs = [r for r in results if isinstance(r, Result)]
    metric_objs = [m for m in results if isinstance(m, Metric)]

    assert any("User" in r.summary for r in result_objs)
    assert any("System" in r.summary for r in result_objs)
    assert any("Total CPU" in r.summary for r in result_objs)

    metric_names = [m.name for m in metric_objs]
    assert "user" in metric_names
    assert "system" in metric_names
    assert "util" in metric_names


def test_cadvisor_cpu_check_with_levels(parsed: Mapping[str, float]) -> None:
    params = {"util": (50.0, 80.0)}
    results = list(check_cadvisor_cpu(params=params, section=parsed))

    result_objs = [r for r in results if isinstance(r, Result)]
    for r in result_objs:
        assert r.state == State.OK


def test_cadvisor_cpu_discovery_empty_section() -> None:
    result = list(discover_cadvisor_cpu({}))
    assert len(result) == 0


def test_cadvisor_cpu_parse_function() -> None:
    string_table = [
        [
            '{"cpu_user": [{"value": "0.10996819381471273", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}], "cpu_system": [{"value": "0.12688637747851422", "labels": {"name": "k8s_coredns_coredns-5c98db65d4-b47gr_kube-system_736910b3-0b55-4c11-8291-f9db987489e3_5"}, "host_selection_label": "name"}]}'
        ]
    ]
    result = parse_cadvisor_cpu(string_table)
    assert "cpu_user" in result
    assert "cpu_system" in result
    assert abs(result["cpu_user"] - 0.10996819381471273) < 1e-10
    assert abs(result["cpu_system"] - 0.12688637747851422) < 1e-10


def test_cadvisor_cpu_parse_multiple_entries() -> None:
    string_table = [
        ['{"cpu_user": [{"value": "0.1"}, {"value": "0.2"}], "cpu_system": [{"value": "0.15"}]}']
    ]
    result = parse_cadvisor_cpu(string_table)
    assert "cpu_system" in result
    assert "cpu_user" not in result
    assert result["cpu_system"] == 0.15


def test_cadvisor_cpu_parse_invalid_value() -> None:
    string_table = [['{"cpu_user": [{"no_value": "0.1"}], "cpu_system": [{"value": "0.15"}]}']]
    result = parse_cadvisor_cpu(string_table)
    assert "cpu_system" in result
    assert "cpu_user" not in result
    assert result["cpu_system"] == 0.15
