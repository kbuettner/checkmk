#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import logging

from cmk.ccc.site import SiteId
from cmk.post_rename_site.registry import rename_action_registry, RenameAction


def handler(old_site_id: SiteId, new_site_id: SiteId, logger: logging.Logger) -> None:
    pass


rename_action_registry.register(
    RenameAction(
        name="test",
        title="test",
        sort_index=20,
        handler=handler,
    )
)
