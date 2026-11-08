<template>
  <div class="card question-card" @click="go">
    <h3>{{ q.title }}</h3>
    <p class="content">{{ q.content }}</p>
    <div class="meta">
      <StatusTag :status="q.status" />
      <span class="count">{{ q.answer_count }} 个回答</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import StatusTag from './StatusTag.vue'

const props = defineProps({ q: { type: Object, required: true } })
const router = useRouter()

function go() {
  router.push({ name: 'question', params: { id: props.q.id } })
}
</script>

<style scoped>
.question-card {
  cursor: pointer;
}
.content {
  color: #666;
  margin: 4px 0 8px;
}
.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.count {
  font-size: 13px;
  color: #999;
}
</style>
