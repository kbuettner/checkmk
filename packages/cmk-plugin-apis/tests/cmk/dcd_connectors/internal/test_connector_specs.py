#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.dcd_connectors.internal import ConnectorSpec, entry_point_prefixes


def test_connector_spec_stores_all_fields() -> None:
    spec = ConnectorSpec(name="test", connector_class=object)
    assert spec.name == "test"
    assert spec.connector_class is object
    assert spec.connector_object_class is None


def test_connector_spec_with_connector_object_class() -> None:
    spec = ConnectorSpec(
        name="test",
        connector_class=object,
        connector_object_class=int,
    )
    assert spec.connector_object_class is int


def test_connector_spec_name_used_by_discovery() -> None:
    spec = ConnectorSpec(name="my_connector", connector_class=object)
    assert spec.name == "my_connector"


def test_entry_point_prefixes_contains_connector_spec() -> None:
    prefixes = entry_point_prefixes()
    assert ConnectorSpec in prefixes


def test_entry_point_prefix_for_connector_spec() -> None:
    prefixes = entry_point_prefixes()
    assert prefixes[ConnectorSpec] == "connector_"
