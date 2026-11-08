<template>
  <div class="container">
    <div v-for="n in items" :key="n.id" class="card notice" @click="read(n)">
      <span class="tag">{{ n.is_read ? '已读' : '未读' }}</span>
      <span>滚木（{{ n.type }}）</span>
      <router-link
        v-if="n.question_id"
        :to="{ name: 'question', params: { id: n.question_id } }"
      >
        查看
      </router-link>
    </div>
    <p v-if="!items.length" class="empty">滚木</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const items = ref([])

async function load() {
  const { data } = await api.listNotifications()
  items.value = data
}

async function read(n) {
  if (n.is_read) return
  await api.readNotification(n.id)
  n.is_read = true
}

onMounted(load)
</script>

<style scoped>
.notice {
  display: flex;
  align-items: center;
  gap: 8px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 24px 0;
}
</style>
