#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import abc
from collections.abc import Sized
from functools import partial
from typing import final, TypeVar

import cmk.ccc.resulttype as result
from cmk.ccc.exceptions import MKFetcherError, MKTimeout

from ._abstract import Fetcher, Mode
from .filecache import FileCache

__all__ = ["PlainFetcherTrigger", "FetcherTrigger"]

_TRawData = TypeVar("_TRawData", bound=Sized)


class FetcherTrigger(abc.ABC):
    @final
    def get_raw_data(
        self, file_cache: FileCache[_TRawData], fetcher: Fetcher[_TRawData], mode: Mode
    ) -> result.Result[_TRawData, Exception]:
        try:
            cached = file_cache.read(mode)
            if cached is not None:
                return result.OK(cached)

            if file_cache.simulation:
                raise MKFetcherError(f"{fetcher}: data unavailable in simulation mode")

            fetched: result.Result[_TRawData, Exception] = result.Error(
                MKFetcherError("unknown error")
            )
            fetched = self._trigger(fetcher, mode)
            fetched.map(partial(file_cache.write, mode=mode))
            return fetched

        except MKTimeout:
            raise

        except Exception as exc:
            return result.Error(exc)

    @abc.abstractmethod
    def _trigger(
        self, fetcher: Fetcher[_TRawData], mode: Mode
    ) -> result.Result[_TRawData, Exception]:
        """Abstract method to be implemented by subclasses to trigger the fetcher."""
        raise NotImplementedError("Subclasses must implement this method.")


class PlainFetcherTrigger(FetcherTrigger):
    """A simple trigger that fetches data without any additional logic."""

    def _trigger(
        self, fetcher: Fetcher[_TRawData], mode: Mode
    ) -> result.Result[_TRawData, Exception]:
        with fetcher:
            return fetcher.fetch(mode)
