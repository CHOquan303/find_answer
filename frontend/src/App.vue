<template>
  <div class="layout">
    <TopNav @toggle-nav="navOpen = !navOpen" />
    <div class="body">
      <SideNav :open="navOpen" @close="navOpen = false" />
      <main class="main">
        <router-view />
      </main>
      <RightRail v-if="route.meta.rail" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import TopNav from './components/TopNav.vue'
import SideNav from './components/SideNav.vue'
import RightRail from './components/RightRail.vue'

const route = useRoute()
const navOpen = ref(false)
</script>

<style scoped>
.body {
  max-width: 1080px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 180px 1fr 200px;
  gap: 20px;
  padding: 20px 16px;
  align-items: start;
}
.main {
  min-width: 0;
}
@media (max-width: 959px) {
  .body {
    grid-template-columns: 1fr;
    padding: 12px 16px;
  }
}
</style>
