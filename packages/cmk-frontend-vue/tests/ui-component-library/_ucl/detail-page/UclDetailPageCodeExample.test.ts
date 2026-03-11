/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclDetailPageCodeExample from '@ucl/_ucl/components/detail-page/UclDetailPageCodeExample.vue'

test('renders Code example heading', () => {
  render(UclDetailPageCodeExample, { props: { code: 'const x = 1' } })
  screen.getByText('Code example')
})

test('renders the provided code string', () => {
  render(UclDetailPageCodeExample, { props: { code: '<CmkButton>Click me</CmkButton>' } })
  screen.getByText('<CmkButton>Click me</CmkButton>')
})
