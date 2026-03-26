<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
export type AuthMethod = 'none' | 'basicauth'

export interface Credential {
  username: string
  password: string // password store ID
}

export interface AuthConfig {
  method: AuthMethod
  credential: Credential | null
}

export interface EndpointConfig {
  address: string
  port: number | undefined
}
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'

import { fetchRestAPI } from '@/lib/cmkFetch.ts'
import usei18n from '@/lib/i18n'

import CmkDropdown from '@/components/CmkDropdown/CmkDropdown.vue'
import CmkLabel from '@/components/CmkLabel.vue'
import type { Suggestion } from '@/components/CmkSuggestions'
import CmkTabs, { CmkTab, CmkTabContent } from '@/components/CmkTabs'
import CmkParagraph from '@/components/typography/CmkParagraph.vue'
import CmkInlineValidation from '@/components/user-input/CmkInlineValidation.vue'
import CmkInput from '@/components/user-input/CmkInput.vue'
import CmkLabelRequired from '@/components/user-input/CmkLabelRequired.vue'

const { _t } = usei18n()

const props = defineProps<{
  noAuthAllowed: boolean
  endpointConfigAllowed: boolean
}>()

const grpcAuth = defineModel<AuthConfig>('grpcAuth', { required: true })
const httpAuth = defineModel<AuthConfig>('httpAuth', { required: true })
const grpcEndpoint = defineModel<EndpointConfig>('grpcEndpoint', { required: true })
const httpEndpoint = defineModel<EndpointConfig>('httpEndpoint', { required: true })

const activeTab = ref('grpc')
const availablePasswords = ref<Suggestion[]>([])
const displayErrors = ref(false)

onMounted(async () => {
  try {
    const response = await fetchRestAPI(
      'api/v1/domain-types/passwordstore_password/collections/passwordstore_password',
      'GET'
    )
    const data = await response.json()
    availablePasswords.value = data.value.map((p: { id: string; title: string }) => ({
      name: p.id,
      title: p.title
    }))
  } catch {
    // password store unavailable — leave list empty
  }
})

const authMethodOptions = computed<Suggestion[]>(() => {
  if (!props.noAuthAllowed) {
    return [{ name: 'basicauth', title: _t('Basic authentication') }]
  }
  return [
    { name: 'none', title: _t('No authentication') },
    { name: 'basicauth', title: _t('Basic authentication') }
  ]
})

watch(
  () => grpcAuth.value.method,
  (method) => {
    if (method === 'basicauth' && grpcAuth.value.credential === null) {
      grpcAuth.value.credential = { username: '', password: '' }
    }
  },
  { immediate: true }
)

watch(
  () => httpAuth.value.method,
  (method) => {
    if (method === 'basicauth' && httpAuth.value.credential === null) {
      httpAuth.value.credential = { username: '', password: '' }
    }
  },
  { immediate: true }
)

function credentialUsernameErrors(credential: Credential): string[] {
  if (!displayErrors.value) {
    return []
  }
  if (!credential.username.trim()) {
    return [_t('Username is required but not specified.')]
  }
  return []
}

function credentialPasswordErrors(credential: Credential): string[] {
  if (!displayErrors.value) {
    return []
  }
  if (!credential.password) {
    return [_t('Password is required but not specified.')]
  }
  return []
}

const grpcUsernameErrors = computed(() =>
  grpcAuth.value.credential ? credentialUsernameErrors(grpcAuth.value.credential) : []
)
const grpcPasswordErrors = computed(() =>
  grpcAuth.value.credential ? credentialPasswordErrors(grpcAuth.value.credential) : []
)
const httpUsernameErrors = computed(() =>
  httpAuth.value.credential ? credentialUsernameErrors(httpAuth.value.credential) : []
)
const httpPasswordErrors = computed(() =>
  httpAuth.value.credential ? credentialPasswordErrors(httpAuth.value.credential) : []
)

const bothEndpointsEmpty = computed(
  () => !grpcEndpoint.value.address.trim() && !httpEndpoint.value.address.trim()
)

const grpcAddressErrors = computed((): string[] => {
  if (!displayErrors.value) {
    return []
  }
  if (!grpcEndpoint.value.address.trim()) {
    return bothEndpointsEmpty.value ? [_t('Enter a valid IP address or host name.')] : []
  }
  return validateAddress(grpcEndpoint.value.address)
})
const grpcPortErrors = computed((): string[] => {
  if (!displayErrors.value) return []
  if (grpcEndpoint.value.port !== undefined || grpcEndpoint.value.address.trim()) {
    return validatePort(grpcEndpoint.value.port)
  }
  return []
})
const httpAddressErrors = computed((): string[] => {
  if (!displayErrors.value) {
    return []
  }
  if (!httpEndpoint.value.address.trim()) {
    return bothEndpointsEmpty.value ? [_t('Enter a valid IP address or host name.')] : []
  }
  return validateAddress(httpEndpoint.value.address)
})
const httpPortErrors = computed((): string[] => {
  if (!displayErrors.value) return []
  if (httpEndpoint.value.port !== undefined || httpEndpoint.value.address.trim()) {
    return validatePort(httpEndpoint.value.port)
  }
  return []
})

function tabHasErrors(auth: AuthConfig): boolean {
  if (auth.method !== 'basicauth') {
    return false
  }
  return !auth.credential?.username.trim() || !auth.credential?.password
}

function isValidIpOrHostname(value: string): boolean {
  const ipv4Match = value.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/)
  if (ipv4Match) {
    return ipv4Match.slice(1).every((p) => parseInt(p, 10) <= 255)
  }
  if (value.includes(':')) {
    return /^[0-9a-fA-F:]+$/.test(value) && value.split(':').length >= 2
  }
  const h = value.endsWith('.') ? value.slice(0, -1) : value
  if (!h || h.length > 253) {
    return false
  }
  const labels = h.split('.')
  if (/^\d+$/.test(labels[labels.length - 1] ?? '')) {
    return false
  }
  return labels.every((l) => l.length > 0 && /^(?!-)[a-z0-9-]{1,63}(?<!-)$/i.test(l))
}

const validateAddress = (value: string): string[] => {
  if (!value.trim()) {
    return [_t('Enter a valid IP address or host name.')]
  }
  if (!isValidIpOrHostname(value)) {
    return [_t('Your input is not a valid host name or IP address.')]
  }
  return []
}

const validatePort = (value: number | undefined): string[] => {
  if (value === undefined || value < 1 || value > 65535) {
    return [_t('Enter a valid port number (example: 1234).')]
  }
  return []
}

function endpointIsConfigured(endpoint: EndpointConfig): boolean {
  return !!endpoint.address.trim()
}

function configuredEndpointHasErrors(endpoint: EndpointConfig): boolean {
  return !isValidIpOrHostname(endpoint.address) || validatePort(endpoint.port).length > 0
}

function validate(): boolean {
  displayErrors.value = true
  if (!props.endpointConfigAllowed) {
    return !tabHasErrors(grpcAuth.value) && !tabHasErrors(httpAuth.value)
  }
  const grpcConfigured = endpointIsConfigured(grpcEndpoint.value)
  const httpConfigured = endpointIsConfigured(httpEndpoint.value)
  if (!grpcConfigured && !httpConfigured) {
    return false
  }
  const grpcValid = !grpcConfigured || !configuredEndpointHasErrors(grpcEndpoint.value)
  const httpValid = !httpConfigured || !configuredEndpointHasErrors(httpEndpoint.value)
  return !tabHasErrors(grpcAuth.value) && !tabHasErrors(httpAuth.value) && grpcValid && httpValid
}

defineExpose({ validate })
</script>

<template>
  <CmkTabs v-model="activeTab">
    <template #tabs>
      <CmkTab id="grpc">{{ _t('GRPC') }}</CmkTab>
      <CmkTab id="http">{{ _t('HTTP') }}</CmkTab>
    </template>
    <template #tab-contents>
      <CmkTabContent id="grpc">
        <CmkParagraph>{{
          _t('Configure a GRPC-based OTLP receiver that will collect OpenTelemetry data.')
        }}</CmkParagraph>

        <div class="mode-otel-configure-collector__form">
          <template v-if="endpointConfigAllowed">
            <CmkLabel>{{ _t('IP address or host name') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="grpcEndpoint.address"
              type="text"
              field-size="MEDIUM"
              :placeholder="_t('0.0.0.0')"
              :external-errors="grpcAddressErrors"
            />
            <CmkLabel>{{ _t('Port') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="grpcEndpoint.port"
              type="number"
              :external-errors="grpcPortErrors"
              :placeholder="_t('4317')"
            />
          </template>

          <CmkLabel>{{ _t('Authentication method') }}</CmkLabel>
          <CmkDropdown
            v-model:selected-option="grpcAuth.method"
            :options="{ type: 'fixed', suggestions: authMethodOptions }"
            :label="_t('Authentication method')"
          />

          <template v-if="grpcAuth.method === 'basicauth' && grpcAuth.credential !== null">
            <span />
            <div class="mode-otel-configure-collector__sub-field">
              <CmkLabel>{{ _t('Username') }} <CmkLabelRequired /></CmkLabel>
              <CmkInput
                v-model="grpcAuth.credential.username"
                type="text"
                field-size="MEDIUM"
                :placeholder="_t('Username')"
                :external-errors="grpcUsernameErrors"
              />

              <CmkLabel>{{ _t('Password') }} <CmkLabelRequired /></CmkLabel>
              <div class="mode-otel-configure-collector__password-row">
                <CmkDropdown
                  v-model:selected-option="grpcAuth.credential.password"
                  :options="{ type: 'fixed', suggestions: availablePasswords }"
                  :input-hint="_t('Select password')"
                  :label="_t('Password')"
                  :form-validation="grpcPasswordErrors.length > 0"
                  :no-elements-text="_t('No passwords available')"
                />
                <!-- enable when password creation flow is implemented -->
                <button type="button" disabled class="mode-otel-configure-collector__btn-create">
                  {{ _t('+ Create') }}
                </button>
              </div>
              <CmkInlineValidation
                v-if="grpcPasswordErrors.length"
                class="mode-otel-configure-collector__password-error"
                :validation="grpcPasswordErrors"
              />
            </div>
          </template>
        </div>
      </CmkTabContent>

      <CmkTabContent id="http">
        <CmkParagraph>{{
          _t('Configure an HTTP-based OTLP receiver that will collect OpenTelemetry data.')
        }}</CmkParagraph>

        <div class="mode-otel-configure-collector__form">
          <template v-if="endpointConfigAllowed">
            <CmkLabel>{{ _t('IP address or host name') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="httpEndpoint.address"
              type="text"
              field-size="MEDIUM"
              :placeholder="_t('0.0.0.0')"
              :external-errors="httpAddressErrors"
            />
            <CmkLabel>{{ _t('Port') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="httpEndpoint.port"
              type="number"
              :external-errors="httpPortErrors"
              :placeholder="_t('4318')"
            />
          </template>

          <CmkLabel>{{ _t('Authentication method') }}</CmkLabel>
          <CmkDropdown
            v-model:selected-option="httpAuth.method"
            :options="{ type: 'fixed', suggestions: authMethodOptions }"
            :label="_t('Authentication method')"
          />

          <template v-if="httpAuth.method === 'basicauth' && httpAuth.credential !== null">
            <span />
            <div class="mode-otel-configure-collector__sub-field">
              <CmkLabel>{{ _t('Username') }} <CmkLabelRequired /></CmkLabel>
              <CmkInput
                v-model="httpAuth.credential.username"
                type="text"
                field-size="MEDIUM"
                :placeholder="_t('Username')"
                :external-errors="httpUsernameErrors"
              />

              <CmkLabel>{{ _t('Password') }} <CmkLabelRequired /></CmkLabel>
              <div class="mode-otel-configure-collector__password-row">
                <CmkDropdown
                  v-model:selected-option="httpAuth.credential.password"
                  :options="{ type: 'fixed', suggestions: availablePasswords }"
                  :input-hint="_t('Select password')"
                  :label="_t('Password')"
                  :form-validation="httpPasswordErrors.length > 0"
                  :no-elements-text="_t('No passwords available')"
                />
                <!-- enable when password creation flow is implemented -->
                <button type="button" disabled class="mode-otel-configure-collector__btn-create">
                  {{ _t('+ Create') }}
                </button>
              </div>
              <CmkInlineValidation
                v-if="httpPasswordErrors.length"
                class="mode-otel-configure-collector__password-error"
                :validation="httpPasswordErrors"
              />
            </div>
          </template>
        </div>
      </CmkTabContent>
    </template>
  </CmkTabs>
</template>

<style scoped>
.mode-otel-configure-collector__form {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--spacing) var(--dimension-6);
  align-items: start;
  margin-top: var(--spacing);
}

.mode-otel-configure-collector__password-row {
  display: flex;
  gap: var(--spacing);
  align-items: center;
}

.mode-otel-configure-collector__password-error {
  grid-column: 2;
}

.mode-otel-configure-collector__btn-create {
  cursor: pointer;
}

.mode-otel-configure-collector__btn-create:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
