#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.legacy_checks.aws_elb import check_aws_elb_statistics


def test_check_aws_elb_statistics() -> None:
    parsed = {
        "RequestCount": 693.235,
        "SurgeQueueLength": 1024.0,
        "SpilloverCount": 0.058333333333333334,
        "Latency": 4.2748083637903225e-06,
        "HealthyHostCount": 1.8,
        "UnHealthyHostCount": 0.0,
        "BackendConnectionErrors": 0.058333333333333334,
    }
    result = list(check_aws_elb_statistics(None, {}, parsed))  # type: ignore[no-untyped-call]
    assert len(result) == 2
    assert result[0][0] == 0  # state OK
    assert "Surge queue length: 1024" in result[0][1]
    assert result[1][0] == 0  # state OK
    assert "Spillover: 0.058/s" in result[1][1]
