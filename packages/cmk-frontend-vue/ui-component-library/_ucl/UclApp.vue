<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import { ref, watch } from 'vue'
import { RouterView } from 'vue-router'
import { useRoute } from 'vue-router'

import UclFooter from './components/UclFooter.vue'
import UclHeader from './components/UclHeader.vue'
import UclNavigation from './components/UclNavigation.vue'
import { useLegacyCss } from './composables/useLegacyCss'

useLegacyCss()

const currentRoute = useRoute()
const screenshotMode = ref(currentRoute.query.screenshot === 'true')

watch(
  () => currentRoute.query.screenshot,
  (screenshot) => {
    screenshotMode.value = screenshot === 'true'
  }
)
</script>

<template>
  <div v-if="!screenshotMode" class="cmk-vue-app ucl">
    <header class="ucl-app__header">
      <UclHeader />
    </header>

    <div class="ucl-app__body">
      <aside class="ucl-app__sidebar">
        <UclNavigation />
      </aside>

      <main class="ucl-app__main">
        <div class="ucl-app__area">
          <RouterView />
        </div>

        <footer class="ucl-app__footer">
          <UclFooter
            title="Design System documentation"
            subtitle="Explore detailed guidelines, usage principles, and processes in our Design System documentation. This space provides additional context to help you design, build, and maintain consistent components."
            button-text="View documentation"
            button-url="https://www.checkmk.com"
          />
        </footer>
      </main>
    </div>
  </div>
  <RouterView v-else />
</template>

<style scoped>
.ucl-app {
  display: flex;
  flex-direction: column;
  color: var(--ucl-body-text-color);
  background-color: var(--ucl-app-bg-color);
  height: 100vh;
  overflow: hidden;
}

.ucl-app__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 24px;
  background-color: var(--ucl-header-bg-color);
  border-bottom: 1px solid var(--ucl-elements-border-color);
  height: 50px;
}

.ucl-app__body {
  display: flex;
  flex: 1;
  overflow: hidden;
  padding: 16px;
  gap: 16px;
}

.ucl-app__sidebar {
  display: flex;
  flex-direction: column;
  width: 250px;
  border-right: 1px solid var(--ucl-elements-border-color);
  overflow: hidden auto;
  flex-shrink: 0;
  scrollbar-width: thin;
  scrollbar-color: var(--ucl-nav-tree-scroll-bar-color) transparent;
}

.ucl-app__sidebar::-webkit-scrollbar {
  width: 6px;
}

.ucl-app__sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.ucl-app__sidebar::-webkit-scrollbar-thumb {
  background-color: var(--ucl-nav-tree-scroll-bar-color);
  border-radius: 20px;
}

.ucl-app__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden auto;
}

.ucl-app__main::-webkit-scrollbar {
  width: 6px;
}

.ucl-app__main::-webkit-scrollbar-track {
  background: transparent;
}

.ucl-app__main::-webkit-scrollbar-thumb {
  background-color: var(--ucl-nav-tree-scroll-bar-color);
  border-radius: 20px;
}

.ucl-app__area {
  flex: 1;
  padding: 16px;
}

.ucl-app__footer {
  margin-top: auto;
  padding: 0 16px 32px;
}
</style>
