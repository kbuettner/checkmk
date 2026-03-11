/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclDetailPageHeader from '@ucl/_ucl/components/detail-page/UclDetailPageHeader.vue'

test('renders slot content as heading', () => {
  render(UclDetailPageHeader, { slots: { default: 'CmkButton' } })
  screen.getByRole('heading', { name: 'CmkButton' })
})
