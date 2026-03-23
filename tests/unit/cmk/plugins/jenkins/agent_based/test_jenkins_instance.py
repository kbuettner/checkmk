#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json

import pytest

from cmk.agent_based.v2 import Result, Service, State
from cmk.plugins.jenkins.agent_based.jenkins_instance import (
    check_jenkins_instance,
    discover_jenkins_instance,
    JenkinsInstance,
    parse_jenkins_instance,
)


@pytest.fixture(scope="module", name="section")
def _section() -> JenkinsInstance:
    return parse_jenkins_instance(
        [
            [
                json.dumps(
                    {
                        "quietingDown": False,
                        "nodeDescription": "the master Jenkins node",
                        "numExecutors": 10,
                        "mode": "NORMAL",
                        "_class": "hudson.model.Hudson",
                        "useSecurity": True,
                    }
                )
            ]
        ]
    )


def test_discovery(section: JenkinsInstance) -> None:
    assert list(discover_jenkins_instance(section)) == [Service()]


def test_check_jenkins_instance(section: JenkinsInstance) -> None:
    assert list(check_jenkins_instance({}, section)) == [
        Result(state=State.OK, summary="Description: The Master Jenkins Node"),
        Result(state=State.OK, summary="Quieting Down: no"),
        Result(state=State.OK, summary="Security used: yes"),
    ]
