/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclAccessibilityTable from '@ucl/_ucl/components/detail-page/UclAccessibilityTable.vue'

test('shows empty message when no data', () => {
  render(UclAccessibilityTable, { props: { data: [] } })
  screen.getByText('No keyboard accessibility available for this component')
})

test('renders key and description for each item', () => {
  const data = [
    { keys: ['Enter'], description: 'Confirms selection' },
    { keys: ['Escape'], description: 'Closes dialog' }
  ]
  render(UclAccessibilityTable, { props: { data } })

  screen.getByText('Enter')
  screen.getByText('Confirms selection')
  screen.getByText('Escape')
  screen.getByText('Closes dialog')
})

test('renders combined key group with separator', () => {
  const data = [{ keys: [['Ctrl', 'Enter']], description: 'Submit form' }]
  render(UclAccessibilityTable, { props: { data } })

  screen.getByText('Ctrl')
  screen.getByText('Enter')
  screen.getByText('+')
  screen.getByText('Submit form')
})
