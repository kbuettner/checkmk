<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkIconButton from '@/components/CmkIconButton.vue'
import CmkInlineButton from '@/components/user-input/CmkInlineButton.vue'

defineOptions({
  inheritAttrs: false
})

defineProps<{
  addElementLabel: string | undefined
  addElement: () => void
}>()
</script>

<template>
  <CmkInlineButton v-if="addElementLabel!!" @click="addElement">
    {{ addElementLabel }}
  </CmkInlineButton>
  <CmkIconButton v-else name="plus" @click="addElement" />
</template>
