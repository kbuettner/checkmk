/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { fireEvent, render, screen } from '@testing-library/vue'
import { defineComponent } from 'vue'

import CmkInlineButton from '@/components/user-input/CmkInlineButton.vue'

const submitHandler = vi.fn((e) => e.preventDefault())

beforeEach(() => {
  document.addEventListener('submit', submitHandler)
})

afterEach(() => {
  submitHandler.mockClear()
  document.removeEventListener('submit', submitHandler)
})

test('CmkInlineButton does not submit form without click callback', async () => {
  const testComponent = defineComponent({
    components: { CmkInlineButton },
    template: `
      <form>
        <CmkInlineButton name="foo" />
      </form>
    `
  })
  render(testComponent)
  const button = screen.getByRole('button')
  await fireEvent.click(button)
  expect(submitHandler).not.toHaveBeenCalled()
})

test('CmkInlineButton disabled prevents click callback', async () => {
  let clicked: boolean = false
  const testComponent = defineComponent({
    components: { CmkInlineButton },
    setup() {
      const onclick = () => {
        clicked = true
      }
      return { onclick }
    },
    template: `
      <form>
        <CmkInlineButton name="foo" :disabled="true" @click="onclick" />
      </form>
    `
  })
  render(testComponent)
  const button = screen.getByRole('button')
  expect(button).toBeDisabled()
  await fireEvent.click(button)
  expect(clicked).toBe(false)
})

test('CmkInlineButton does not submit form with click callback', async () => {
  let clicked: boolean = false
  const testComponent = defineComponent({
    components: { CmkInlineButton },
    setup() {
      const onclick = () => {
        clicked = true
      }
      return { onclick }
    },
    template: `
      <form>
        <CmkInlineButton name="foo" @click="onclick" />
      </form>
    `
  })
  render(testComponent)
  const button = screen.getByRole('button')
  await fireEvent.click(button)
  expect(clicked).toBe(true)
  expect(submitHandler).not.toHaveBeenCalled()
})
