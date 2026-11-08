<template>
  <div class="search-view">
    <div class="title-row">
      <h2>搜索结果</h2>
    </div>
    <p v-if="!q" class="empty">滚木</p>
    <div v-else class="list">
      <div
        v-for="item in items"
        :key="item.id"
        class="result"
        @click="go(item.id)"
      >
        <span class="r-title">{{ item.title }}</span>
        <StatusTag :status="item.status" />
        <span class="r-time">{{ (item.created_at || '').slice(0, 10) }}</span>
      </div>
    </div>
    <p v-if="q && !items.length" class="empty">滚木</p>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import StatusTag from '../components/StatusTag.vue'

const route = useRoute()
const router = useRouter()
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

function go(id) {
  router.push({ name: 'question', params: { id } })
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
.title-row {
  margin-bottom: 12px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 24px 0;
}
.result {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #fff;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}
.r-title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.r-time {
  font-size: 13px;
  color: #999;
  flex-shrink: 0;
}
</style>
