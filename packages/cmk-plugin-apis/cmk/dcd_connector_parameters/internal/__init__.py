#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

r"""
WARNING
-------

**This version of the API is work in progress and not yet stable.
It is not recommended to use this version in production systems.**


Scope
-----

This API provides functionality to create DCD connector parameter specifications
that can be discovered by Checkmk's GUI.

To be discovered, a plug-in module must be placed in the ``dcd_connector_parameters``
subdirectory of a plug-in family (e.g.
``cmk/plugins/<family>/dcd_connector_parameters/<module>.py``) and the plug-in instance
name must start with the corresponding prefix.
"""

from collections.abc import Mapping

from . import connector_parameter_specs


def entry_point_prefixes() -> Mapping[type[connector_parameter_specs.ConnectorParametersSpec], str]:
    """Return the types of plug-ins and their respective prefixes that can be discovered by Checkmk.

    These types can be used to create plug-ins that can be discovered by Checkmk.
    To be discovered, the plug-in must be of one of the types returned by this function and its name
    must start with the corresponding prefix.

    Example:
    ********

    >>> for plugin_type, prefix in entry_point_prefixes().items():
    ...     print(f'{prefix}... = {plugin_type.__name__}(...)')
    connector_params_... = ConnectorParametersSpec(...)
    """
    return {
        connector_parameter_specs.ConnectorParametersSpec: "connector_params_",
    }


__all__ = [
    "connector_parameter_specs",
    "entry_point_prefixes",
]
