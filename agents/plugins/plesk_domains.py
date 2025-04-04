#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

__version__ = "2.5.0b1"

# Lists all domains configured in plesk
#
# <<<plesk_domains>>>
# <domain>

import sys

try:
    import MySQLdb  # type: ignore[import-untyped]
except ImportError as e:
    sys.stdout.write(
        "<<<plesk_domains>>>\n%s. Please install missing module via `pip install mysqlclient`.\n"
        % e
    )
    sys.exit(0)

with open("/etc/psa/.psa.shadow") as pwd_file:
    pwd = pwd_file.read().strip()
try:
    db = MySQLdb.connect(
        host="localhost",
        db="psa",
        user="admin",
        passwd=pwd,
        charset="utf8",
    )
except MySQLdb.Error as e:
    sys.stderr.write("MySQL-Error %d: %s\n" % (e.args[0], e.args[1]))
    sys.exit(1)

cursor = db.cursor()
cursor.execute("SELECT name FROM domains")
sys.stdout.write("<<<plesk_domains>>>\n")
sys.stdout.write("%s\n" % "\n".join([d[0] for d in cursor.fetchall()]))
cursor.close()
