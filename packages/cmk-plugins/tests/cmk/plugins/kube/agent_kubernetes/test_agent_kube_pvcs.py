#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="type-arg"
# mypy: disable-error-code="name-defined"
# mypy: disable-error-code="untyped-decorator"
# mypy: disable-error-code="misc"

from typing import Any

import pytest
from kubernetes import client

from cmk.plugins.kube.transform import (
    persistent_volume_claim_from_client,
)
from tests.cmk.plugins.kube.agent_kubernetes.utils import FakeResponse
from tests.cmk.plugins.kube.data.kube_1_34 import (
    pvc_with_volume_attributes_class_name,
    pvc_without_volume_attributes_class_name,
)


class TestPVCs:
    @pytest.mark.parametrize(
        "data, expected_name, expected_volume_attributes_class_name",
        [
            (
                pvc_with_volume_attributes_class_name.DATA,
                "test-pvc",
                "silver",
            ),
            (
                pvc_without_volume_attributes_class_name.DATA,
                "test-pvc",
                None,
            ),
        ],
    )
    def test_parse_full_pvc_json(
        self,
        data: dict[str, Any],
        expected_name: str,
        expected_volume_attributes_class_name: str | None,
        core_client: client.CoreV1Api,
    ) -> None:
        """
        Test that we can load a raw PersistentVolumeClaim response from Kube
        successfully into schemata.api objects.
        """
        raw_pvc = core_client.api_client.deserialize(FakeResponse(data), "V1PersistentVolumeClaim")
        pvc = persistent_volume_claim_from_client(raw_pvc)

        assert pvc.metadata.name == expected_name
        assert (
            pvc.status.current_volume_attributes_class_name == expected_volume_attributes_class_name
        )
