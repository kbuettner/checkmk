#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# No stub file
import pytest

import cmk.gui.inventory
import cmk.gui.utils
from cmk.gui.inventory.filters import FilterInvtableText, FilterInvtableVersion
from cmk.gui.num_split import cmp_version
from cmk.gui.views.inventory._display_hints import (
    _cmp_inv_generic,
    _decorate_sort_function,
    _get_related_legacy_hints,
    _parse_view_name,
    _RelatedLegacyHints,
    AttributeDisplayHint,
    ColumnDisplayHint,
    inv_display_hints,
    NodeDisplayHint,
)
from cmk.gui.views.inventory._paint_functions import (
    inv_paint_generic,
    inv_paint_if_oper_status,
    inv_paint_number,
    inv_paint_service_status,
    inv_paint_size,
)
from cmk.gui.views.inventory.registry import inventory_displayhints
from cmk.utils.structured_data import SDKey, SDNodeName, SDPath


def test_display_hint_titles() -> None:
    assert all("title" in hint for hint in inventory_displayhints.values())


_IGNORED_KEYS_BY_PATH = {
    ("hardware", "system"): ["serial_number", "model_name"],
    ("hardware", "storage", "disks"): [
        "drive_index",
        "bus",
        "serial",
        "local",
        "size",
        "product",
        "type",
        "vendor",
    ],
    ("software", "applications", "vmwareesx"): ["clusters"],
}


def test_related_display_hints() -> None:
    # Each node of a display hint (especially for table columns or attributes) must have a display
    # hint, too.
    # Example:
    #   If you add the attribute hint
    #       ".software.applications.fritz.link_type"
    #   then the following hints must exist:
    #       ".software.applications.fritz.",
    #       ".software.applications.",
    #       ".software.",

    # XOR: We have either
    #   - real nodes, eg. ".hardware.chassis.",
    #   - nodes with attributes, eg. ".hardware.cpu." or
    #   - nodes with a table, eg. ".software.packages:"

    all_related_legacy_hints = _get_related_legacy_hints(inventory_displayhints)

    def _check_path(path: SDPath) -> bool:
        return all(path[:idx] in all_related_legacy_hints for idx in range(1, len(path)))

    def _check_legacy_hints(related_legacy_hints: _RelatedLegacyHints) -> bool:
        return bool(related_legacy_hints.for_node) ^ bool(related_legacy_hints.for_table)

    def _check_table_key_order(path: SDPath, related_legacy_hints: _RelatedLegacyHints) -> bool:
        ignored_keys = set(_IGNORED_KEYS_BY_PATH.get(path, []))
        return (
            set(related_legacy_hints.for_table.get("keyorder", [])) - ignored_keys
            == set(related_legacy_hints.by_column) - ignored_keys
        )

    def _check_attributes_key_order(
        path: SDPath, related_legacy_hints: _RelatedLegacyHints
    ) -> bool:
        ignored_keys = set(_IGNORED_KEYS_BY_PATH.get(path, []))
        return (
            set(related_legacy_hints.for_node.get("keyorder", [])) - ignored_keys
            == set(related_legacy_hints.by_key) - ignored_keys
        )

    for path, related_legacy_hints in _get_related_legacy_hints(inventory_displayhints).items():
        assert _check_path(path)
        assert _check_legacy_hints(related_legacy_hints)
        assert _check_table_key_order(path, related_legacy_hints)
        assert _check_attributes_key_order(path, related_legacy_hints)


def test_missing_table_keyorder() -> None:
    ignore_paths = [
        ".hardware.memory.arrays:",  # Has no table
        ".software.applications.vmwareesx:",
    ]

    missing_keyorders = [
        path
        for path, hint in inventory_displayhints.items()
        if path.endswith(":") and path not in ignore_paths and not hint.get("keyorder")
    ]

    # TODO test second part
    assert missing_keyorders == [], (
        "Missing 'keyorder' in %s. The 'keyorder' should contain at least the key columns."
        % ",".join(missing_keyorders)
    )


@pytest.mark.parametrize(
    "val_a, val_b, result",
    [
        (None, None, 0),
        (None, 0, -1),
        (0, None, 1),
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, -1),
    ],
)
def test__cmp_inv_generic(val_a: object, val_b: object, result: int) -> None:
    assert _decorate_sort_function(_cmp_inv_generic)(val_a, val_b) == result


@pytest.mark.parametrize(
    "path, expected_node_hint",
    [
        (
            (),
            NodeDisplayHint(
                path=(),
                icon="",
                title="Inventory tree",
                short_title="Inventory tree",
                long_title="Inventory tree",
                attributes={},
                columns={},
                table_view_name="",
                table_is_show_more=True,
            ),
        ),
        (
            ("hardware",),
            NodeDisplayHint(
                path=(SDNodeName("hardware"),),
                icon="hardware",
                title="Hardware",
                short_title="Hardware",
                long_title="Hardware",
                attributes={},
                columns={},
                table_view_name="",
                table_is_show_more=True,
            ),
        ),
        (
            ("hardware", "cpu"),
            NodeDisplayHint(
                path=(SDNodeName("hardware"), SDNodeName("cpu")),
                icon="",
                title="Processor",
                short_title="Processor",
                long_title="Hardware ➤ Processor",
                # The single attribute hints are not checked here
                attributes={
                    SDKey("arch"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("max_speed"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("model"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("type"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("threads"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("smt_threads"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("cpu_max_capa"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("cpus"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("logical_cpus"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("cores"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("cores_per_cpu"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("threads_per_cpu"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("cache_size"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("bus_speed"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("voltage"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("sharing_mode"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("implementation_mode"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                    SDKey("entitlement"): AttributeDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        data_type="",
                        is_show_more=False,
                    ),
                },
                columns={},
                table_view_name="",
                table_is_show_more=True,
            ),
        ),
        (
            ("software", "applications", "docker", "images"),
            NodeDisplayHint(
                path=(
                    SDNodeName("software"),
                    SDNodeName("applications"),
                    SDNodeName("docker"),
                    SDNodeName("images"),
                ),
                icon="",
                title="Docker images",
                short_title="Docker images",
                long_title="Docker ➤ Docker images",
                attributes={},
                # The single column hints are not checked here
                columns={
                    SDKey("id"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("creation"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("size"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("labels"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("amount_containers"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("repotags"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("repodigests"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                },
                table_view_name="invdockerimages",
                table_is_show_more=False,
            ),
        ),
        (
            ("path", "to", "node"),
            NodeDisplayHint(
                path=(SDNodeName("path"), SDNodeName("to"), SDNodeName("node")),
                icon="",
                title="Node",
                short_title="Node",
                long_title="To ➤ Node",
                attributes={},
                columns={},
                table_view_name="",
                table_is_show_more=True,
            ),
        ),
    ],
)
def test_make_node_displayhint(path: SDPath, expected_node_hint: NodeDisplayHint) -> None:
    node_hint = inv_display_hints.get_node_hint(path)

    assert node_hint.ident == "_".join(("inv",) + node_hint.path)
    assert node_hint.icon == expected_node_hint.icon
    assert node_hint.title == expected_node_hint.title
    assert node_hint.long_title == expected_node_hint.long_title
    assert node_hint.long_inventory_title == expected_node_hint.long_inventory_title

    assert list(node_hint.attributes) == list(expected_node_hint.attributes)
    assert list(node_hint.columns) == list(expected_node_hint.columns)

    assert node_hint.table_view_name == expected_node_hint.table_view_name
    assert node_hint.table_is_show_more == expected_node_hint.table_is_show_more


@pytest.mark.parametrize(
    "raw_path, expected_node_hint",
    [
        (
            ".foo.bar.",
            NodeDisplayHint(
                path=(SDNodeName("foo"), SDNodeName("bar")),
                icon="",
                title="Bar",
                short_title="Bar",
                long_title="Foo ➤ Bar",
                attributes={},
                columns={},
                table_is_show_more=True,
                table_view_name="",
            ),
        ),
        (
            ".foo.bar:",
            NodeDisplayHint(
                path=(SDNodeName("foo"), SDNodeName("bar")),
                icon="",
                title="Bar",
                short_title="Bar",
                long_title="Foo ➤ Bar",
                attributes={},
                columns={},
                table_is_show_more=True,
                table_view_name="",
            ),
        ),
        (
            ".software.",
            NodeDisplayHint(
                path=(SDNodeName("software"),),
                icon="software",
                title="Software",
                short_title="Software",
                long_title="Software",
                attributes={},
                columns={},
                table_view_name="",
                table_is_show_more=True,
            ),
        ),
        (
            ".software.applications.docker.containers:",
            NodeDisplayHint(
                path=(
                    SDNodeName("software"),
                    SDNodeName("applications"),
                    SDNodeName("docker"),
                    SDNodeName("containers"),
                ),
                icon="",
                title="Docker containers",
                short_title="Docker containers",
                long_title="Docker ➤ Docker containers",
                attributes={},
                # The single column hints are not checked here
                columns={
                    SDKey("id"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("creation"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("name"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("labels"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("status"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                    SDKey("image"): ColumnDisplayHint(
                        title="",
                        short_title="",
                        long_title="",
                        paint_function=lambda *args: ("", ""),
                        sort_function=lambda *args: 0,
                        filter_class=FilterInvtableText,
                    ),
                },
                table_view_name="invdockercontainers",
                table_is_show_more=False,
            ),
        ),
    ],
)
def test_make_node_displayhint_from_hint(
    raw_path: str, expected_node_hint: NodeDisplayHint
) -> None:
    node_hint = inv_display_hints.get_node_hint(
        cmk.gui.inventory.parse_internal_raw_path(raw_path).path
    )

    assert node_hint.ident == "_".join(("inv",) + node_hint.path)
    assert node_hint.icon == expected_node_hint.icon
    assert node_hint.title == expected_node_hint.title
    assert node_hint.long_title == expected_node_hint.long_title
    assert node_hint.long_inventory_title == expected_node_hint.long_inventory_title

    assert list(node_hint.attributes) == list(expected_node_hint.attributes)
    assert list(node_hint.columns) == list(expected_node_hint.columns)

    assert node_hint.table_view_name == expected_node_hint.table_view_name
    assert node_hint.table_is_show_more == expected_node_hint.table_is_show_more


@pytest.mark.parametrize(
    "path, key, expected",
    [
        (
            (),
            "key",
            ColumnDisplayHint(
                title="Key",
                short_title="Key",
                long_title="Key",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ("networking", "interfaces"),
            "oper_status",
            ColumnDisplayHint(
                title="Operational status",
                short_title="Operational status",
                long_title="Network interfaces ➤ Operational status",
                paint_function=inv_paint_if_oper_status,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ("path", "to", "node"),
            "key",
            ColumnDisplayHint(
                title="Key",
                short_title="Key",
                long_title="Node ➤ Key",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ("software", "applications", "check_mk", "sites"),
            "cmc",
            ColumnDisplayHint(
                title="CMC status",
                short_title="CMC",
                long_title="Checkmk sites ➤ CMC status",
                paint_function=inv_paint_service_status,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
    ],
)
def test_make_column_displayhint(path: SDPath, key: str, expected: ColumnDisplayHint) -> None:
    hint = inv_display_hints.get_node_hint(path).get_column_hint(key)
    assert hint.title == expected.title
    assert hint.short_title == expected.short_title
    assert hint.long_title == expected.long_title
    assert hint.long_inventory_title == expected.long_inventory_title
    assert callable(hint.paint_function)
    assert callable(hint.sort_function)


@pytest.mark.parametrize(
    "raw_path, expected",
    [
        (
            ".foo:*.bar",
            ColumnDisplayHint(
                title="Bar",
                short_title="Bar",
                long_title="Foo ➤ Bar",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ".software.packages:*.package_version",
            ColumnDisplayHint(
                title="Package version",
                short_title="Package version",
                long_title="Software packages ➤ Package version",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(cmp_version),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ".software.packages:*.version",
            ColumnDisplayHint(
                title="Version",
                short_title="Version",
                long_title="Software packages ➤ Version",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(cmp_version),
                filter_class=FilterInvtableVersion,
            ),
        ),
        (
            ".networking.interfaces:*.index",
            ColumnDisplayHint(
                title="Index",
                short_title="Index",
                long_title="Network interfaces ➤ Index",
                paint_function=inv_paint_number,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
        (
            ".networking.interfaces:*.oper_status",
            ColumnDisplayHint(
                title="Operational status",
                short_title="Operational status",
                long_title="Network interfaces ➤ Operational status",
                paint_function=inv_paint_if_oper_status,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                filter_class=FilterInvtableText,
            ),
        ),
    ],
)
def test_make_column_displayhint_from_hint(raw_path: str, expected: ColumnDisplayHint) -> None:
    inventory_path = cmk.gui.inventory.parse_internal_raw_path(raw_path)
    hint = inv_display_hints.get_node_hint(inventory_path.path).get_column_hint(
        inventory_path.key or ""
    )
    assert hint.title == expected.title
    assert hint.short_title == expected.short_title
    assert hint.long_title == expected.long_title
    assert hint.long_inventory_title == expected.long_inventory_title
    assert callable(hint.paint_function)
    assert callable(hint.sort_function)


@pytest.mark.parametrize(
    "path, key, expected",
    [
        (
            (),
            "key",
            AttributeDisplayHint(
                title="Key",
                short_title="Key",
                long_title="Key",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="str",
                is_show_more=True,
            ),
        ),
        (
            ("hardware", "storage", "disks"),
            "size",
            AttributeDisplayHint(
                title="Size",
                short_title="Size",
                long_title="Block devices ➤ Size",
                paint_function=inv_paint_size,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="size",
                is_show_more=True,
            ),
        ),
        (
            ("path", "to", "node"),
            "key",
            AttributeDisplayHint(
                title="Key",
                short_title="Key",
                long_title="Node ➤ Key",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="str",
                is_show_more=True,
            ),
        ),
    ],
)
def test_make_attribute_displayhint(path: SDPath, key: str, expected: AttributeDisplayHint) -> None:
    hint = inv_display_hints.get_node_hint(path).get_attribute_hint(key)
    assert hint.data_type == expected.data_type
    assert callable(hint.paint_function)
    assert callable(hint.sort_function)
    assert hint.title == expected.title
    assert hint.long_title == expected.long_title
    assert hint.long_inventory_title == expected.long_inventory_title
    assert hint.is_show_more == expected.is_show_more


@pytest.mark.parametrize(
    "raw_path, expected",
    [
        (
            ".foo.bar",
            AttributeDisplayHint(
                title="Bar",
                short_title="Bar",
                long_title="Foo ➤ Bar",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="str",
                is_show_more=True,
            ),
        ),
        (
            ".hardware.cpu.arch",
            AttributeDisplayHint(
                title="CPU architecture",
                short_title="CPU architecture",
                long_title="Processor ➤ CPU architecture",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="str",
                is_show_more=True,
            ),
        ),
        (
            ".hardware.system.product",
            AttributeDisplayHint(
                title="Product",
                short_title="Product",
                long_title="System ➤ Product",
                paint_function=inv_paint_generic,
                sort_function=_decorate_sort_function(_cmp_inv_generic),
                data_type="str",
                is_show_more=False,
            ),
        ),
    ],
)
def test_make_attribute_displayhint_from_hint(
    raw_path: str, expected: AttributeDisplayHint
) -> None:
    inventory_path = cmk.gui.inventory.parse_internal_raw_path(raw_path)
    hint = inv_display_hints.get_node_hint(inventory_path.path).get_attribute_hint(
        inventory_path.key or ""
    )
    assert hint.data_type == expected.data_type
    assert callable(hint.paint_function)
    assert callable(hint.sort_function)
    assert hint.title == expected.title
    assert hint.long_title == expected.long_title
    assert hint.long_inventory_title == expected.long_inventory_title
    assert hint.is_show_more == expected.is_show_more


@pytest.mark.parametrize(
    "view_name, expected_view_name",
    [
        ("", ""),
        ("viewname", "invviewname"),
        ("invviewname", "invviewname"),
        ("viewname_of_host", "invviewname"),
        ("invviewname_of_host", "invviewname"),
    ],
)
def test__parse_view_name(view_name: str, expected_view_name: str) -> None:
    assert _parse_view_name(view_name) == expected_view_name
