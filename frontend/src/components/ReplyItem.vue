<template>
  <div class="reply">
    <p class="content">{{ reply.author.real_name }}: {{ reply.content }}</p>
    <button v-if="isLoggedIn" @click="show = !show">回复</button>
    <div v-if="show" class="form">
      <input v-model="content" />
      <button @click="submit">提交</button>
    </div>
    <div class="children">
      <ReplyItem
        v-for="c in reply.children"
        :key="c.id"
        :reply="c"
        :answer-id="answerId"
        @refresh="$emit('refresh')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  reply: { type: Object, required: true },
  answerId: { type: Number, required: true },
})
const emit = defineEmits(['refresh'])

const auth = useAuthStore()
const isLoggedIn = auth.isLoggedIn

const show = ref(false)
const content = ref('')

async function submit() {
  const text = content.value.trim()
  if (!text) return
  await api.createReply(props.answerId, { content: text, parent_id: props.reply.id })
  content.value = ''
  show.value = false
  emit('refresh')
}
</script>

<style scoped>
.reply {
  border-left: 2px solid #eee;
  padding-left: 12px;
  margin-top: 10px;
}
.content {
  margin-bottom: 6px;
}
.form {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
.form input {
  flex: 1;
  width: auto;
}
.children {
  margin-left: 12px;
}
</style>
