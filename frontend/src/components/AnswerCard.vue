<template>
  <div class="card answer-card">
    <div class="head">
      <span class="author">{{ answer.author.real_name }}</span>
      <ConfidenceBadge :title="answer.author.confidence_title" />
    </div>
    <p class="content">{{ answer.content }}</p>
    <p v-if="answer.is_accepted" class="accepted">[已采纳]</p>
    <div class="actions">
      <span class="likes">点赞 {{ answer.like_count }}</span>
      <button v-if="isLoggedIn" @click="like">点赞</button>
      <button v-if="isLoggedIn" @click="report">举报</button>
      <button v-if="isQuestioner && !answer.is_accepted" @click="accept">采纳</button>
      <button v-if="isLoggedIn" @click="showReply = !showReply">追问</button>
    </div>

    <div v-if="showReply" class="reply-form">
      <input v-model="replyContent" />
      <button @click="submitReply">提交追问</button>
    </div>

    <div class="replies">
      <ReplyItem
        v-for="r in answer.replies"
        :key="r.id"
        :reply="r"
        :answer-id="answer.id"
        @refresh="$emit('refresh')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import ConfidenceBadge from './ConfidenceBadge.vue'
import ReplyItem from './ReplyItem.vue'

const props = defineProps({
  answer: { type: Object, required: true },
  questionId: { type: Number, required: true },
  isQuestioner: { type: Boolean, default: false },
})
const emit = defineEmits(['refresh'])

const auth = useAuthStore()
const isLoggedIn = auth.isLoggedIn

const showReply = ref(false)
const replyContent = ref('')

async function like() {
  await api.likeAnswer(props.answer.id)
  emit('refresh')
}

async function accept() {
  await api.acceptAnswer(props.questionId, props.answer.id)
  emit('refresh')
}

async function report() {
  const reason = window.prompt('滚木（举报原因）')
  if (!reason) return
  await api.reportAnswer(props.answer.id, { reason })
  window.alert('滚木（已提交）')
}

async function submitReply() {
  const text = replyContent.value.trim()
  if (!text) return
  await api.createReply(props.answer.id, { content: text })
  replyContent.value = ''
  showReply.value = false
  emit('refresh')
}
</script>

<style scoped>
.head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.author {
  font-weight: 600;
}
.content {
  margin-bottom: 8px;
}
.accepted {
  color: #666;
  margin-bottom: 8px;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.likes {
  font-size: 13px;
  color: #999;
}
.reply-form {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
.reply-form input {
  flex: 1;
  width: auto;
}
.replies {
  margin-top: 4px;
}
</style>
