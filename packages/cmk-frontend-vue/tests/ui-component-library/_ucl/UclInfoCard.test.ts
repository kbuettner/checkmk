/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclInfoCard from '@ucl/_ucl/components/UclInfoCard.vue'

test('renders title', () => {
  render(UclInfoCard, { props: { title: 'Card title' } })
  screen.getByText('Card title')
})

test('renders subtitle when provided', () => {
  render(UclInfoCard, { props: { title: 'Card title', subtitle: 'Helpful description' } })
  screen.getByText('Helpful description')
})

test('does not render subtitle when not provided', () => {
  render(UclInfoCard, { props: { title: 'Card title' } })
  expect(screen.queryByText('Helpful description')).toBeNull()
})

test('renders bullet points when provided', () => {
  render(UclInfoCard, {
    props: { title: 'Card title', bulletPoints: ['First point', 'Second point'] }
  })
  screen.getByText('First point')
  screen.getByText('Second point')
})

test('renders no list when bulletPoints is empty', () => {
  const { container } = render(UclInfoCard, { props: { title: 'Card title', bulletPoints: [] } })
  expect(container.querySelector('ul')).toBeNull()
})
