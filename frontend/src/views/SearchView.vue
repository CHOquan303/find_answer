<template>
  <div class="container">
    <SearchBar />
    <p v-if="!q" class="empty">滚木</p>
    <div v-for="item in items" :key="item.id" class="card result">
      <router-link :to="{ name: 'question', params: { id: item.id } }">
        {{ item.title }}
      </router-link>
    </div>
    <p v-if="q && !items.length" class="empty">滚木</p>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import SearchBar from '../components/SearchBar.vue'

const route = useRoute()
const q = ref(route.query.q || '')
const items = ref([])

async function load() {
  if (!q.value) {
    items.value = []
    return
  }
  const { data } = await api.search(q.value)
  items.value = data.items
}

watch(
  () => route.query.q,
  (v) => {
    q.value = v || ''
    load()
  }
)

onMounted(load)
</script>

<style scoped>
.empty {
  text-align: center;
  color: #999;
  padding: 24px 0;
}
.result {
  padding: 12px 16px;
}
</style>
