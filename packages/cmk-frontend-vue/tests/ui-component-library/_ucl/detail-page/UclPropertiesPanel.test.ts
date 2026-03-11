/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render, screen } from '@testing-library/vue'
import UclPropertiesPanel from '@ucl/_ucl/components/detail-page/UclPropertiesPanel.vue'
import type { PanelConfig } from '@ucl/_ucl/types/prop-panel'

vi.mock('vue-router', () => ({
  useRouter: () => ({ resolve: () => ({ href: '/' }) }),
  useRoute: () => ({ query: {} })
}))

test('renders Properties heading', () => {
  render(UclPropertiesPanel, { props: { config: {}, modelValue: {} } })
  screen.getByText('Properties')
})

test('renders label for a boolean prop', () => {
  const config: PanelConfig = {
    enabled: { type: 'boolean', title: 'Enabled', initialState: false }
  }
  render(UclPropertiesPanel, { props: { config, modelValue: { enabled: false } } })
  screen.getByText('Enabled')
})

test('renders text input for a string prop', () => {
  const config: PanelConfig = {
    label: { type: 'string', title: 'Label', initialState: 'default' }
  }
  render(UclPropertiesPanel, { props: { config, modelValue: { label: 'default' } } })
  screen.getByRole('textbox')
})

test('renders number input for a number prop', () => {
  const config: PanelConfig = {
    count: { type: 'number', title: 'Count', initialState: 3 }
  }
  render(UclPropertiesPanel, { props: { config, modelValue: { count: 3 } } })
  expect(screen.getByRole('spinbutton')).toHaveValue(3)
})

test('renders textarea for a multiline-string prop', () => {
  const config: PanelConfig = {
    description: { type: 'multiline-string', title: 'Description', initialState: '' }
  }
  render(UclPropertiesPanel, { props: { config, modelValue: { description: '' } } })
  expect(screen.getByRole('textbox').tagName).toBe('TEXTAREA')
})

test('renders labels for all props in config', () => {
  const config: PanelConfig = {
    enabled: { type: 'boolean', title: 'Enabled', initialState: true },
    label: { type: 'string', title: 'Label text', initialState: '' }
  }
  render(UclPropertiesPanel, { props: { config, modelValue: { enabled: true, label: '' } } })

  screen.getByText('Enabled')
  screen.getByText('Label text')
})
