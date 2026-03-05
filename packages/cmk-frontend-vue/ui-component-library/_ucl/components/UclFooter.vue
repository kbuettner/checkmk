<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { computed } from 'vue'

import CmkButton from '@/components/CmkButton.vue'

import ctaBackgroundImageModernDark from '../assets/images/cta-banner-bg-dark.png'
import ctaBackgroundImageFacelift from '../assets/images/cta-banner-bg-light.png'
import { useTheme } from '../composables/useTheme'

const props = defineProps<{
  title: string
  subtitle?: string
  buttonText: string
  buttonUrl: string
}>()

const { getByTheme } = useTheme()

const ctaBackgroundImage = computed(() => {
  return getByTheme(ctaBackgroundImageFacelift, ctaBackgroundImageModernDark)
})

const handleButtonClick = () => {
  window.open(props.buttonUrl, '_blank', 'noopener,noreferrer')
}
</script>

<template>
  <div class="ucl-footer" :style="{ backgroundImage: `url(${ctaBackgroundImage})` }">
    <div class="ucl-footer__content">
      <h2 class="ucl-footer__title">{{ title }}</h2>
      <p class="ucl-footer__subtitle">{{ subtitle }}</p>
      <CmkButton variant="primary" @click="handleButtonClick">
        {{ buttonText }}
      </CmkButton>
    </div>
  </div>
</template>

<style scoped>
.ucl-footer {
  background-size: contain;
  background-position: left center;
  background-repeat: no-repeat;
  background-color: var(--ucl-elements-background-color);
  border-radius: 4px;
  padding: 40px 40px 40px 200px;
  display: flex;
  align-items: center;
  min-height: 200px;
}

.ucl-footer__content {
  position: relative;
  max-width: 700px;
}

.ucl-footer__title {
  font-size: 24px;
  line-height: normal;
  margin: 0 0 12px;
}

.ucl-footer__subtitle {
  line-height: 20px;
  margin: 0 0 24px;
}
</style>
