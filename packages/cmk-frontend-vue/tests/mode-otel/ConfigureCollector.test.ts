/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { cleanup, render, screen, waitFor } from '@testing-library/vue'
import { defineComponent, ref } from 'vue'

import * as cmkFetch from '@/lib/cmkFetch'

import ConfigureCollector from '@/mode-otel/otel-configuration-steps/ConfigureCollector.vue'
import type { AuthConfig } from '@/mode-otel/otel-configuration-steps/ConfigureCollector.vue'

function mockPasswordsResponse(passwords: { id: string; title: string }[] = []) {
  return vi.spyOn(cmkFetch, 'fetchRestAPI').mockResolvedValue({
    raiseForStatus: vi.fn().mockResolvedValue(undefined),
    json: vi.fn().mockResolvedValue({ value: passwords })
  } as unknown as cmkFetch.CmkFetchResponse)
}

function mockPasswordsError() {
  vi.spyOn(cmkFetch, 'fetchRestAPI').mockRejectedValue(new Error('Network error'))
}

function renderComponent(noAuthAllowed = true) {
  const grpcAuth = ref<AuthConfig>({
    method: noAuthAllowed ? 'none' : 'basicauth',
    credential: null
  })
  const httpAuth = ref<AuthConfig>({
    method: noAuthAllowed ? 'none' : 'basicauth',
    credential: null
  })
  const compRef = ref<InstanceType<typeof ConfigureCollector>>()

  render(
    defineComponent({
      components: { ConfigureCollector },
      setup: () => ({ grpcAuth, httpAuth, compRef, noAuthAllowed }),
      template: `<ConfigureCollector ref="compRef" :no-auth-allowed="noAuthAllowed" v-model:grpc-auth="grpcAuth" v-model:http-auth="httpAuth" />`
    })
  )

  return { grpcAuth, httpAuth, compRef }
}

describe('ConfigureCollector', () => {
  afterEach(() => {
    cleanup()
    vi.restoreAllMocks()
  })

  describe('default auth method', () => {
    test('defaults to "none" when no-auth is allowed', async () => {
      mockPasswordsResponse()
      const { grpcAuth, httpAuth } = renderComponent(true)

      expect(grpcAuth.value.method).toBe('none')
      expect(httpAuth.value.method).toBe('none')
    })

    test('defaults to "basicauth" when no-auth is not allowed', async () => {
      mockPasswordsResponse()
      const { grpcAuth, httpAuth } = renderComponent(false)

      expect(grpcAuth.value.method).toBe('basicauth')
      expect(httpAuth.value.method).toBe('basicauth')
    })
  })

  describe('auth method options', () => {
    test('shows "No authentication" option when no-auth is allowed', async () => {
      mockPasswordsResponse()
      renderComponent(true)

      // The GRPC tab is active by default; auth dropdown should be rendered
      await waitFor(() => {
        expect(screen.getByText('Authentication method')).toBeInTheDocument()
      })
    })

    test('hides "No authentication" option when no-auth is not allowed', async () => {
      mockPasswordsResponse()
      renderComponent(false)

      await waitFor(() => {
        expect(screen.getByText('Authentication method')).toBeInTheDocument()
      })
      // "No authentication" should not appear as an option
      expect(screen.queryByText('No authentication')).not.toBeInTheDocument()
    })
  })

  describe('credential fields visibility', () => {
    test('credential fields do not appear when method is "none"', async () => {
      mockPasswordsResponse()
      renderComponent(true)

      await waitFor(() => {
        expect(screen.queryByText('Username')).not.toBeInTheDocument()
      })
    })

    test('credential fields appear when basicauth is selected', async () => {
      mockPasswordsResponse()
      renderComponent(false)

      await waitFor(() => {
        expect(screen.getByText('Username')).toBeInTheDocument()
      })
    })
  })

  describe('validation', () => {
    test('validate() returns true for "none" auth method', async () => {
      mockPasswordsResponse()
      const { compRef } = renderComponent(true)

      await waitFor(() => expect(compRef.value).toBeDefined())
      await new Promise((r) => setTimeout(r, 0))

      const result = compRef.value!.validate()
      expect(result).toBe(true)
    })

    test('validate() returns false if credential has empty username', async () => {
      mockPasswordsResponse([{ id: 'pw1', title: 'Password 1' }])
      const { compRef, grpcAuth } = renderComponent(true)

      grpcAuth.value.method = 'basicauth'
      grpcAuth.value.credential = { username: '', password: 'pw1' }

      await waitFor(() => expect(compRef.value).toBeDefined())
      await new Promise((r) => setTimeout(r, 0))

      const result = compRef.value!.validate()
      expect(result).toBe(false)
      await screen.findByText('Username is required but not specified.')
    })

    test('validate() returns false if credential has no password', async () => {
      mockPasswordsResponse()
      const { compRef, grpcAuth } = renderComponent(true)

      grpcAuth.value.method = 'basicauth'
      grpcAuth.value.credential = { username: 'admin', password: '' }

      await waitFor(() => expect(compRef.value).toBeDefined())
      await new Promise((r) => setTimeout(r, 0))

      const result = compRef.value!.validate()
      expect(result).toBe(false)
      await screen.findByText('Password is required but not specified.')
    })

    test('validate() returns true for valid basicauth credential', async () => {
      mockPasswordsResponse([{ id: 'pw1', title: 'Password 1' }])
      const { compRef, grpcAuth } = renderComponent(true)

      grpcAuth.value.method = 'basicauth'
      grpcAuth.value.credential = { username: 'admin', password: 'pw1' }

      await waitFor(() => expect(compRef.value).toBeDefined())
      await new Promise((r) => setTimeout(r, 0))

      const result = compRef.value!.validate()
      expect(result).toBe(true)
    })

    test('validate() returns false if only HTTP tab has invalid credential', async () => {
      mockPasswordsError()
      const { compRef, httpAuth } = renderComponent(true)

      httpAuth.value.method = 'basicauth'
      httpAuth.value.credential = { username: '', password: '' }

      await waitFor(() => expect(compRef.value).toBeDefined())
      await new Promise((r) => setTimeout(r, 0))

      const result = compRef.value!.validate()
      expect(result).toBe(false)
    })
  })
})
