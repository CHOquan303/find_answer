<template>
  <div v-for="n in items" :key="n.id" @click="read(n)">
    <span>[{{ n.is_read ? '已读' : '未读' }}]</span>
    <span>滚木（{{ n.type }}）</span>
    <router-link
      v-if="n.question_id"
      :to="{ name: 'question', params: { id: n.question_id } }"
    >
      查看
    </router-link>
  </div>
  <p v-if="!items.length">滚木</p>
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
