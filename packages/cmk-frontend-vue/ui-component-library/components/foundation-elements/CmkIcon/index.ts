/**
 * Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { Page } from '@ucl/_ucl/types/page'

import UclCmkIcon from './UclCmkIcon.vue'
import UclCmkIconEmblem from './UclCmkIconEmblem.vue'
import UclCmkMultitoneIcon from './UclCmkMultitoneIcon.vue'

export const pages = [
  new Page('CmkIcon', UclCmkIcon),
  new Page('CmkIconEmblem', UclCmkIconEmblem),
  new Page('CmkMultitoneIcon', UclCmkMultitoneIcon)
]
