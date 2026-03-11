/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclFooter from '@ucl/_ucl/components/UclFooter.vue'

test('renders title as heading', () => {
  render(UclFooter, { props: { title: 'Stay connected', buttonText: 'Visit', buttonUrl: '#' } })
  screen.getByRole('heading', { name: 'Stay connected' })
})

test('renders subtitle when provided', () => {
  render(UclFooter, {
    props: {
      title: 'Title',
      subtitle: 'Learn more about Checkmk',
      buttonText: 'Go',
      buttonUrl: '#'
    }
  })
  screen.getByText('Learn more about Checkmk')
})

test('renders button with correct label', () => {
  render(UclFooter, { props: { title: 'Title', buttonText: 'Visit our website', buttonUrl: '#' } })
  screen.getByRole('button', { name: 'Visit our website' })
})
