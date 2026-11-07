<template>
  <div @click="go">
    <h3>{{ q.title }}</h3>
    <p>{{ q.content }}</p>
    <StatusTag :status="q.status" />
    <span>{{ q.answer_count }} 个回答</span>
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
