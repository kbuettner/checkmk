#!/usr/bin/env python3
# Copyright (C) 2021 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Callable, Mapping
from dataclasses import dataclass
from logging import Logger
from typing import Protocol

from cmk.ccc.site import SiteId


class Name(str): ...


class Title:
    def __init__(self, raw: str, /) -> None:
        self._raw = raw

    def localize(self, localizer: Callable[[str], str], /) -> str:
        return localizer(self._raw)


class SortIndex(int): ...


class RenameActionHandler(Protocol):
    def __call__(self, old_site_id: SiteId, new_site_id: SiteId, logger: Logger) -> None:
        pass


@dataclass(frozen=True, kw_only=True)
class RenameAction:
    """Plugin class for all site rename operations"""

    name: Name
    title: Title
    sort_index: SortIndex
    run: RenameActionHandler


def entry_point_prefixes() -> Mapping[type[RenameAction], str]:
    return {RenameAction: "rename_action_"}
