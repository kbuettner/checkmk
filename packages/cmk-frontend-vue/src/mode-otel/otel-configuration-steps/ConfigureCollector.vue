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
}>()

const grpcAuth = defineModel<AuthConfig>('grpcAuth', { required: true })
const httpAuth = defineModel<AuthConfig>('httpAuth', { required: true })

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

function tabHasErrors(auth: AuthConfig): boolean {
  if (auth.method !== 'basicauth') {
    return false
  }
  return !auth.credential?.username.trim() || !auth.credential?.password
}

function validate(): boolean {
  displayErrors.value = true
  return !tabHasErrors(grpcAuth.value) && !tabHasErrors(httpAuth.value)
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
          <CmkLabel>{{ _t('Authentication method') }} <CmkLabelRequired /></CmkLabel>
          <CmkDropdown
            v-model:selected-option="grpcAuth.method"
            :options="{ type: 'fixed', suggestions: authMethodOptions }"
            :label="_t('Authentication method')"
            width="fill"
          />
        </div>

        <template v-if="grpcAuth.method === 'basicauth' && grpcAuth.credential !== null">
          <div class="mode-otel-configure-collector__form">
            <CmkLabel>{{ _t('Username') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="grpcAuth.credential.username"
              type="text"
              field-size="FILL"
              :placeholder="_t('username')"
              :external-errors="grpcUsernameErrors"
            />

            <CmkLabel>{{ _t('Password') }} <CmkLabelRequired /></CmkLabel>
            <div class="mode-otel-configure-collector__password-row">
              <CmkDropdown
                v-model:selected-option="grpcAuth.credential.password"
                :options="{ type: 'fixed', suggestions: availablePasswords }"
                :input-hint="_t('Select password')"
                :label="_t('Password')"
                width="fill"
                :form-validation="grpcPasswordErrors.length > 0"
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
      </CmkTabContent>

      <CmkTabContent id="http">
        <CmkParagraph>{{
          _t('Configure an HTTP-based OTLP receiver that will collect OpenTelemetry data.')
        }}</CmkParagraph>

        <div class="mode-otel-configure-collector__form">
          <CmkLabel>{{ _t('Authentication method') }} <CmkLabelRequired /></CmkLabel>
          <CmkDropdown
            v-model:selected-option="httpAuth.method"
            :options="{ type: 'fixed', suggestions: authMethodOptions }"
            :label="_t('Authentication method')"
            width="fill"
          />
        </div>

        <template v-if="httpAuth.method === 'basicauth' && httpAuth.credential !== null">
          <div class="mode-otel-configure-collector__form">
            <CmkLabel>{{ _t('Username') }} <CmkLabelRequired /></CmkLabel>
            <CmkInput
              v-model="httpAuth.credential.username"
              type="text"
              field-size="FILL"
              :placeholder="_t('username')"
              :external-errors="httpUsernameErrors"
            />

            <CmkLabel>{{ _t('Password') }} <CmkLabelRequired /></CmkLabel>
            <div class="mode-otel-configure-collector__password-row">
              <CmkDropdown
                v-model:selected-option="httpAuth.credential.password"
                :options="{ type: 'fixed', suggestions: availablePasswords }"
                :input-hint="_t('Select password')"
                :label="_t('Password')"
                width="fill"
                :form-validation="httpPasswordErrors.length > 0"
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
