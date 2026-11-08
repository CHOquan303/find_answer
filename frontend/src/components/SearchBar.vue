<template>
  <div class="search">
    <input v-model="keyword" @keyup.enter="go" />
    <button @click="go">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const keyword = ref(route.query.q || '')

function go() {
  const q = keyword.value.trim()
  if (q) router.push({ name: 'search', query: { q } })
}
</script>

<style scoped>
.search {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.search input {
  flex: 1;
  width: auto;
}
</style>
