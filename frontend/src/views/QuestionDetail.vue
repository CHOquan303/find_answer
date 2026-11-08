<template>
  <div v-if="detail" class="container">
    <div class="card">
      <h2>{{ detail.title }}</h2>
      <p class="q-content">{{ detail.content }}</p>
      <StatusTag :status="detail.status" />
      <p class="meta">提问者: {{ detail.author.real_name }} · {{ detail.created_at }}</p>
      <button v-if="isQuestioner" @click="resolve">标注已解决</button>
    </div>

    <div v-for="a in detail.answers" :key="a.id">
      <AnswerCard
        :answer="a"
        :question-id="detail.id"
        :is-questioner="isQuestioner"
        @refresh="load"
      />
    </div>
    <p v-if="!detail.answers.length" class="empty">滚木</p>

    <div v-if="canAnswer" class="card answer-form">
      <textarea v-model="answerContent"></textarea>
      <button @click="submitAnswer">回答</button>
    </div>
    <p v-else-if="isLoggedIn" class="empty">滚木（无回答权限）</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import StatusTag from '../components/StatusTag.vue'
import AnswerCard from '../components/AnswerCard.vue'

const route = useRoute()
const auth = useAuthStore()

const detail = ref(null)
const answerContent = ref('')

const isLoggedIn = computed(() => auth.isLoggedIn)
const canAnswer = computed(() => auth.canAnswer)
const isQuestioner = computed(
  () => auth.user && detail.value && auth.user.id === detail.value.author.id
)

async function load() {
  const { data } = await api.getQuestion(route.params.id)
  detail.value = data
}

async function resolve() {
  await api.resolveQuestion(detail.value.id)
  load()
}

async function submitAnswer() {
  const text = answerContent.value.trim()
  if (!text) return
  await api.createAnswer(detail.value.id, { content: text })
  answerContent.value = ''
  load()
}

onMounted(load)
</script>

<style scoped>
.q-content {
  color: #666;
  margin-bottom: 8px;
}
.meta {
  font-size: 13px;
  color: #999;
  margin: 8px 0;
}
.empty {
  text-align: center;
  color: #999;
  padding: 24px 0;
}
.answer-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
