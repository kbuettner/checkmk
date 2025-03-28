#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Runs and observes regular jobs in the cmk.gui context"""

from ._scheduler import load_last_job_runs, save_last_job_runs

__all__ = [
    "load_last_job_runs",
    "save_last_job_runs",
]
