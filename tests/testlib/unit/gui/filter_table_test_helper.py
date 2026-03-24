#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Shared helpers for filter table tests across editions."""

from collections.abc import Mapping, Sequence
from typing import Any, NamedTuple

from cmk.gui.type_defs import Rows
from cmk.inventory.structured_data import deserialize_tree


class FilterTableTest(NamedTuple):
    ident: str
    request_vars: Sequence[tuple[str, str]]
    rows: Rows
    expected_rows: Sequence[Mapping[str, Any]]


filter_table_tests = [
    # Testing base class BIStatusFilter
    FilterTableTest(
        ident="aggr_assumed_state",
        request_vars=[("bias0", "on"), ("bias1", "on"), ("bias_filled", "1")],
        rows=[
            {"aggr_assumed_state": {"state": 0}},
            {"aggr_assumed_state": {"state": 1}},
            {"aggr_assumed_state": {"state": 2}},
        ],
        expected_rows=[
            {"aggr_assumed_state": {"state": 0}},
            {"aggr_assumed_state": {"state": 1}},
        ],
    ),
    # Testing base class Filter
    FilterTableTest(
        ident="aggr_group",
        request_vars=[("aggr_group", "blä")],
        rows=[
            {"aggr_group": "blub"},
            {"aggr_group": "blä"},
        ],
        expected_rows=[
            {"aggr_group": "blä"},
        ],
    ),
    FilterTableTest(
        ident="aggr_hosts",
        request_vars=[
            ("aggr_host_host", "z"),
        ],
        rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "a"), ("s", "c")]},
            {"aggr_hosts": [("s", "a"), ("s", "g")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
        expected_rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
    ),
    FilterTableTest(
        ident="aggr_hosts",
        request_vars=[
            ("aggr_host_site", ""),
            ("aggr_host_host", "z"),
        ],
        rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "a"), ("s", "c")]},
            {"aggr_hosts": [("s", "a"), ("s", "g")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
        expected_rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
    ),
    FilterTableTest(
        ident="aggr_hosts",
        request_vars=[
            ("aggr_host_site", "d"),
            ("aggr_host_host", "z"),
        ],
        rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "a"), ("s", "c")]},
            {"aggr_hosts": [("s", "a"), ("s", "g")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
        expected_rows=[
            {"aggr_hosts": [("s", "a"), ("s", "z")]},
            {"aggr_hosts": [("s", "b"), ("s", "z")]},
        ],
    ),
    # Testing base class BITextFilter
    FilterTableTest(
        ident="aggr_name",
        request_vars=[("aggr_name", "a")],
        rows=[
            {"aggr_name": "a"},
            {"aggr_name": "aaa"},
            {"aggr_name": "b"},
            {"aggr_name": "c"},
        ],
        expected_rows=[
            {"aggr_name": "a"},
        ],
    ),
    # Testing base class FilterTriState
    FilterTableTest(
        ident="aggr_service_used",
        request_vars=[("is_aggr_service_used", "0")],
        rows=[
            {"site": "s", "host_name": "h", "service_description": "srv1"},
            {"site": "s", "host_name": "h", "service_description": "srv2"},
            {"site": "s", "host_name": "h2", "service_description": "srv2"},
        ],
        expected_rows=[
            {"host_name": "h", "service_description": "srv2", "site": "s"},
            {"host_name": "h2", "service_description": "srv2", "site": "s"},
        ],
    ),
    FilterTableTest(
        ident="aggr_service_used",
        request_vars=[("is_aggr_service_used", "1")],
        rows=[
            {"site": "s", "host_name": "h", "service_description": "srv1"},
            {"site": "s", "host_name": "h", "service_description": "srv2"},
            {"site": "s", "host_name": "h2", "service_description": "srv2"},
        ],
        expected_rows=[
            {"site": "s", "host_name": "h", "service_description": "srv1"},
        ],
    ),
    FilterTableTest(
        ident="aggr_service_used",
        request_vars=[("is_aggr_service_used", "-1")],
        rows=[
            {"site": "s", "host_name": "h", "service_description": "srv1"},
            {"site": "s", "host_name": "h", "service_description": "srv2"},
            {"site": "s", "host_name": "h2", "service_description": "srv2"},
            {"site": "b", "host_name": "h", "service_description": "srv1"},
        ],
        expected_rows=[
            {"site": "s", "host_name": "h", "service_description": "srv1"},
            {"site": "s", "host_name": "h", "service_description": "srv2"},
            {"site": "s", "host_name": "h2", "service_description": "srv2"},
            {"site": "b", "host_name": "h", "service_description": "srv1"},
        ],
    ),
    # Testing base class DeploymentTristateFilter
    FilterTableTest(
        ident="deployment_has_agent",
        request_vars=[("is_deployment_has_agent", "0")],
        rows=[
            {"host_name": "abc"},
            {"host_name": "zzz"},
        ],
        expected_rows=[
            {"host_name": "zzz"},
        ],
    ),
    FilterTableTest(
        ident="deployment_has_agent",
        request_vars=[("is_deployment_has_agent", "1")],
        rows=[],
        expected_rows=[],
    ),
    FilterTableTest(
        ident="deployment_has_agent",
        request_vars=[("is_deployment_has_agent", "-1")],
        rows=[
            {"host_name": "abc"},
            {"host_name": "zzz"},
        ],
        expected_rows=[
            {"host_name": "abc"},
            {"host_name": "zzz"},
        ],
    ),
    FilterTableTest(
        ident="discovery_state",
        request_vars=[
            ("discovery_state_ignored", "on"),
            ("discovery_state_vanished", "on"),
            ("discovery_state_unmonitored", ""),
        ],
        rows=[
            {"discovery_state": "ignored"},
            {"discovery_state": "vanished"},
            {"discovery_state": "unmonitored"},
        ],
        expected_rows=[
            {"discovery_state": "ignored"},
            {"discovery_state": "vanished"},
        ],
    ),
    # Testing base class FilterInvtableText
    FilterTableTest(
        ident="invbackplane_description",
        request_vars=[
            ("invbackplane_description", "lulu"),
        ],
        rows=[
            {"invbackplane_description": "lulu"},
            {"invbackplane_description": "lele"},
        ],
        expected_rows=[
            {"invbackplane_description": "lulu"},
        ],
    ),
    # Testing base class FilterInvtableVersion
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
    ),
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[
            ("invswpac_package_version_from", "1.0"),
        ],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
    ),
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[
            ("invswpac_package_version_until", "3.0"),
        ],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
        ],
    ),
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[
            ("invswpac_package_version_from", "1.0"),
            ("invswpac_package_version_until", "3.0"),
        ],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "1.5.1"},
            {"invswpac_package_version": "2.0.0"},
        ],
    ),
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": None},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": None},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
    ),
    FilterTableTest(
        ident="invswpac_package_version",
        request_vars=[
            ("invswpac_package_version_from", "1.0"),
            ("invswpac_package_version_until", "3.0"),
        ],
        rows=[
            {"invswpac_package_version": "0.5"},
            {"invswpac_package_version": "0.5.1"},
            {"invswpac_package_version": None},
            {"invswpac_package_version": "2.0.0"},
            {"invswpac_package_version": "4.5.1"},
        ],
        expected_rows=[
            {"invswpac_package_version": "2.0.0"},
        ],
    ),
    # Testing base class FilterInvtableIDRange
    FilterTableTest(
        ident="invinterface_index",
        request_vars=[
            ("invinterface_index_from", "3"),
            ("invinterface_index_until", "10"),
        ],
        rows=[
            {"invinterface_index": 1},
            {"invinterface_index": 3},
            {"invinterface_index": 5},
            {"invinterface_index": 11},
        ],
        expected_rows=[
            {"invinterface_index": 3},
            {"invinterface_index": 5},
        ],
    ),
    # Testing base class FilterInvtableOperStatus
    FilterTableTest(
        ident="invinterface_oper_status",
        request_vars=[],
        rows=[
            {"invinterface_oper_status": 1},
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
        expected_rows=[
            {"invinterface_oper_status": 1},
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
    ),
    FilterTableTest(
        ident="invinterface_oper_status",
        request_vars=[
            ("invinterface_oper_status_1", ""),
            ("invinterface_oper_status_3", "on"),
            ("invinterface_oper_status_5", ""),
        ],
        rows=[
            {"invinterface_oper_status": 1},
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
        expected_rows=[
            {"invinterface_oper_status": 3},
        ],
    ),
    FilterTableTest(
        ident="invinterface_oper_status",
        request_vars=[
            ("invinterface_oper_status_1", ""),
            ("invinterface_oper_status_3", ""),
            ("invinterface_oper_status_5", ""),
        ],
        rows=[
            {"invinterface_oper_status": 1},
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
        expected_rows=[],
    ),
    FilterTableTest(
        ident="invinterface_oper_status",
        request_vars=[
            ("invinterface_oper_status_1", ""),
            ("invinterface_oper_status_3", "on"),
        ],
        rows=[
            {"invinterface_oper_status": 1},
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
        expected_rows=[
            {"invinterface_oper_status": 3},
            {"invinterface_oper_status": 5},
        ],
    ),
    # Testing base class FilterInvtableAdminStatus
    FilterTableTest(
        ident="invinterface_admin_status",
        request_vars=[
            ("invinterface_admin_status_1", "on"),
            ("invinterface_admin_status_2", ""),
        ],
        rows=[
            {"invinterface_admin_status": "1"},
            {"invinterface_admin_status": "2"},
        ],
        expected_rows=[
            {"invinterface_admin_status": "1"},
        ],
    ),
    FilterTableTest(
        ident="invinterface_admin_status",
        request_vars=[
            ("invinterface_admin_status_1", ""),
            ("invinterface_admin_status_2", "on"),
        ],
        rows=[
            {"invinterface_admin_status": "1"},
            {"invinterface_admin_status": "2"},
        ],
        expected_rows=[
            {"invinterface_admin_status": "2"},
        ],
    ),
    FilterTableTest(
        ident="invinterface_admin_status",
        request_vars=[],
        rows=[
            {"invinterface_admin_status": "1"},
            {"invinterface_admin_status": "2"},
        ],
        expected_rows=[
            {"invinterface_admin_status": "1"},
            {"invinterface_admin_status": "2"},
        ],
    ),
    # Testing base class FilterInvtableAvailable
    FilterTableTest(
        ident="invinterface_available",
        request_vars=[
            ("invinterface_available_True", ""),
            ("invinterface_available_False", "on"),
        ],
        rows=[
            {"invinterface_available": False},
            {"invinterface_available": True},
        ],
        expected_rows=[
            {"invinterface_available": False},
        ],
    ),
    FilterTableTest(
        ident="invinterface_available",
        request_vars=[
            ("invinterface_available_True", "on"),
            ("invinterface_available_False", ""),
        ],
        rows=[
            {"invinterface_available": False},
            {"invinterface_available": True},
        ],
        expected_rows=[
            {"invinterface_available": True},
        ],
    ),
    FilterTableTest(
        ident="invinterface_available",
        request_vars=[],
        rows=[
            {"invinterface_available": False},
            {"invinterface_available": True},
        ],
        expected_rows=[
            {"invinterface_available": False},
            {"invinterface_available": True},
        ],
    ),
    # Testing base class FilterInvtableInterfaceType
    FilterTableTest(
        ident="invinterface_port_type",
        request_vars=[
            ("invinterface_port_type", "2|3|10"),
        ],
        rows=[
            {"invinterface_port_type": "1"},
            {"invinterface_port_type": "2"},
            {"invinterface_port_type": "10"},
        ],
        expected_rows=[
            {"invinterface_port_type": "2"},
            {"invinterface_port_type": "10"},
        ],
    ),
    # Testing base class FilterInvtableTimestampAsAge
    FilterTableTest(
        ident="invinterface_last_change",
        request_vars=[
            ("invinterface_last_change_from", "1"),
            ("invinterface_last_change_from_prefix", "d"),
            ("invinterface_last_change_until", "5"),
            ("invinterface_last_change_until_prefix", "d"),
        ],
        rows=[
            {"invinterface_last_change": 1523811000},
            {"invinterface_last_change": 1523811000 - (60 * 60 * 24 * 10)},
            {"invinterface_last_change": 1523811000 - (60 * 60 * 24 * 4)},
        ],
        expected_rows=[
            {"invinterface_last_change": 1523811000 - (60 * 60 * 24 * 4)},
        ],
    ),
    # FilterECServiceLevelRange
    FilterTableTest(
        ident="svc_service_level",
        request_vars=[("svc_service_level_lower", "1"), ("svc_service_level_upper", "3")],
        rows=[
            {
                "service_custom_variables": {"EC_SL": "0"},
            },
            {
                "service_custom_variables": {"EC_SL": "1"},
            },
            {
                "service_custom_variables": {"EC_SL": "2"},
            },
            {
                "service_custom_variables": {"EC_SL": "3"},
            },
            {
                "service_custom_variables": {"EC_SL": "4"},
            },
        ],
        expected_rows=[
            {
                "service_custom_variables": {"EC_SL": "1"},
            },
            {
                "service_custom_variables": {"EC_SL": "2"},
            },
            {
                "service_custom_variables": {"EC_SL": "3"},
            },
        ],
    ),
    FilterTableTest(
        ident="hst_service_level",
        request_vars=[("hst_service_level_lower", "1")],
        rows=[
            {
                "host_custom_variables": {"EC_SL": "0"},
            },
            {
                "host_custom_variables": {"EC_SL": "1"},
            },
            {
                "host_custom_variables": {"EC_SL": "2"},
            },
        ],
        expected_rows=[
            {
                "host_custom_variables": {"EC_SL": "1"},
            },
        ],
    ),
    FilterTableTest(
        ident="hst_service_level",
        request_vars=[("hst_service_level_upper", "2")],
        rows=[
            {
                "host_custom_variables": {"EC_SL": "0"},
            },
            {
                "host_custom_variables": {"EC_SL": "1"},
            },
            {
                "host_custom_variables": {"EC_SL": "2"},
            },
        ],
        expected_rows=[
            {
                "host_custom_variables": {"EC_SL": "2"},
            },
        ],
    ),
    # TODO: Testing base class FilterHistoric
    # FilterTableTest(
    #    ident="host_metrics_hist",
    #    request_vars=[
    #        ('cutoff', "10"),
    #    ],
    #    rows=[
    #    ],
    #    expected_rows=[
    #    ],
    # ),
]


filter_inv_table_tests = [
    # Filter out filled trees (is_has_inv == 0)
    FilterTableTest(
        ident="has_inv",
        request_vars=[
            ("is_has_inv", "0"),
        ],
        rows=[
            {"host_inventory": deserialize_tree({})},
            {"host_inventory": deserialize_tree({"a": "b"})},
        ],
        expected_rows=[
            {"host_inventory": deserialize_tree({})},
        ],
    ),
    # Filter out empty trees (is_has_inv == 1)
    FilterTableTest(
        ident="has_inv",
        request_vars=[
            ("is_has_inv", "1"),
        ],
        rows=[
            {"host_inventory": deserialize_tree({})},
            {"host_inventory": deserialize_tree({"a": "b"})},
        ],
        expected_rows=[
            {"host_inventory": deserialize_tree({"a": "b"})},
        ],
    ),
    # Do not apply filter (is_has_inv == -1)
    FilterTableTest(
        ident="has_inv",
        request_vars=[
            ("is_has_inv", "-1"),
        ],
        rows=[
            {"host_inventory": deserialize_tree({})},
            {"host_inventory": deserialize_tree({"a": "b"})},
        ],
        expected_rows=[
            {"host_inventory": deserialize_tree({})},
            {"host_inventory": deserialize_tree({"a": "b"})},
        ],
    ),
    # Testing base class FilterInvText
    FilterTableTest(
        ident="inv_software_os_vendor",
        request_vars=[
            ("inv_software_os_vendor", "bla"),
        ],
        rows=[
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "bla"}}})},
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "blabla"}}})},
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "ag blabla"}}})},
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "blu"}}})},
        ],
        expected_rows=[
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "bla"}}})},
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "blabla"}}})},
            {"host_inventory": deserialize_tree({"software": {"os": {"vendor": "ag blabla"}}})},
        ],
    ),
    # Testing base class FilterInvFloat
    FilterTableTest(
        ident="inv_hardware_cpu_bus_speed",
        request_vars=[
            ("inv_hardware_cpu_bus_speed_from", "10"),
            ("inv_hardware_cpu_bus_speed_from_prefix", "M"),
            ("inv_hardware_cpu_bus_speed_until", "20"),
            ("inv_hardware_cpu_bus_speed_until_prefix", "M"),
        ],
        rows=[
            {"host_inventory": deserialize_tree({"hardware": {"cpu": {"bus_speed": 1000000}}})},
            {"host_inventory": deserialize_tree({"hardware": {"cpu": {"bus_speed": 15000000}}})},
            {"host_inventory": deserialize_tree({"hardware": {"cpu": {"bus_speed": 21000000}}})},
        ],
        expected_rows=[
            {"host_inventory": deserialize_tree({"hardware": {"cpu": {"bus_speed": 15000000}}})},
        ],
    ),
]
