/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
// Verifies that the UCL app entry point (index.ts) calls initializeComponentRegistry on startup.
// Without this call, form-spec components that use FormEditDispatcher will throw at render time.
import { expect, it, vi } from 'vitest'
// TODO: flaky in CI due to timeout on dynamic import — rewrite using injection (export start() from index.ts)
import type * as Vue from 'vue'

const initializeSpy = vi.fn()

vi.mock('@/form/private/FormEditDispatcher/dispatch', () => ({
  initializeComponentRegistry: initializeSpy,
  getComponent: vi.fn()
}))

vi.mock('vue', async () => {
  const mod = await vi.importActual<typeof Vue>('vue')
  return { ...mod, createApp: vi.fn(() => ({ use: vi.fn().mockReturnThis(), mount: vi.fn() })) }
})

it.skip('calls initializeComponentRegistry on startup', async () => {
  await import('@ucl/index')
  expect(initializeSpy).toHaveBeenCalledOnce()
})
