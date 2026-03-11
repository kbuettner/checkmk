/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { fireEvent, render, screen } from '@testing-library/vue'
import UclSearch from '@ucl/_ucl/components/UclSearch.vue'

test('renders search input', () => {
  render(UclSearch)
  screen.getByPlaceholderText('Search...')
})

test('shows no results message when query matches nothing', async () => {
  render(UclSearch)
  const input = screen.getByPlaceholderText('Search...')

  await fireEvent.update(input, 'xyznotfound12345')

  screen.getByText('No results found')
})

test('does not show results list when query is empty', () => {
  render(UclSearch)

  expect(screen.queryByText('No results found')).toBeNull()
})

test('clears results when input is emptied', async () => {
  render(UclSearch)
  const input = screen.getByPlaceholderText('Search...')

  await fireEvent.update(input, 'xyznotfound12345')
  await fireEvent.update(input, '')

  expect(screen.queryByText('No results found')).toBeNull()
})
