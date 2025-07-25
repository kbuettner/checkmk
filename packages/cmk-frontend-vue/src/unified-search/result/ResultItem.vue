<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { CmkIconProps } from '@/components/CmkIcon.vue'
import CmkIcon from '@/components/CmkIcon.vue'
import { immediateWatch } from '@/lib/watch'
import { useTemplateRef } from 'vue'
import ResultItemTitle from './ResultItemTitle.vue'
import CmkZebra from '@/components/CmkZebra.vue'

export interface ResultItemProps {
  idx: number
  icon?: CmkIconProps | undefined
  title: string
  html?: string | undefined
  url?: string | undefined
  context?: string | undefined
  focus?: boolean | undefined
  breadcrumb?: string[] | undefined
}
const props = defineProps<ResultItemProps>()

const focusRef = useTemplateRef('item-focus')

immediateWatch(
  () => ({ newFocus: props.focus }),
  async ({ newFocus }) => {
    if (newFocus) {
      focusRef.value?.focus()
    }
  }
)
</script>

<template>
  <li class="result-item">
    <CmkZebra :num="idx">
      <a
        v-if="props.url"
        ref="item-focus"
        :href="props.url"
        target="main"
        class="result-item-handler"
        :class="{ focus: props.focus }"
      >
        <div v-if="props.icon" class="result-item-inner-start">
          <CmkIcon
            :name="props.icon.name"
            :rotate="props.icon.rotate"
            :size="props.icon.size"
            class="result-item-icon"
          ></CmkIcon>
        </div>
        <div class="result-item-inner-end">
          <span
            v-if="props.breadcrumb && props.breadcrumb.length > 0"
            class="result-item-breadcrump"
            >{{ props.breadcrumb.join(' > ') }}</span
          >
          <ResultItemTitle :title="props.html ? props.html : props.title"></ResultItemTitle>
        </div>
      </a>
      <button v-else ref="item-focus" class="result-item-handler" :class="{ focus: props.focus }">
        <div v-if="props.icon" class="result-item-inner-start">
          <CmkIcon
            :name="props.icon.name"
            :rotate="props.icon.rotate"
            :size="props.icon.size"
            class="result-item-icon"
          ></CmkIcon>
        </div>
        <div class="result-item-inner-end">
          <span v-if="props.breadcrumb" class="result-item-breadcrump">{{
            props.breadcrumb.join(' > ')
          }}</span>
          <ResultItemTitle :title="props.html ? props.html : props.title"></ResultItemTitle>
        </div>
      </button>
    </CmkZebra>
  </li>
</template>

<style scoped>
.result-item {
  list-style-type: none;

  .result-item-handler {
    padding: var(--spacing);
    width: calc(100% - 22px);
    margin: 0;
    background: var(--default-bg-color);
    text-decoration: none;
    display: flex;
    flex-direction: row;
    outline-color: var(--success);
    border: 0;
    border-radius: 0px;
    display: flex;
    flex-direction: row;
    box-sizing: content-box;
    border: 1px solid var(--default-bg-color);

    &:hover {
      background-color: var(--ux-theme-5);
      border: 1px solid var(--ux-theme-5);
    }

    &:active,
    &:focus {
      border: 1px solid var(--success);
      outline: none;
    }
  }

  .result-item-inner {
    width: 100%;
    height: 100%;
  }

  .result-item-inner-start {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .result-item-inner-end {
    display: flex;
    flex-direction: column;
  }
}

.result-item-breadcrump {
  text-transform: capitalize;
  margin-bottom: var(--spacing-half);
  font-size: var(--font-size-small);
  color: var(--font-color-dimmed);
}

.result-item-title {
  font-weight: bold;
}

.result-item-icon {
  margin-right: var(--spacing);
}
</style>
