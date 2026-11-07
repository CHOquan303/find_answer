<template>
  <form @submit.prevent="submit">
    <select v-model="categoryId">
      <option :value="null">滚木（分类可选）</option>
      <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>
    <input v-model="title" placeholder="标题" />
    <textarea v-model="content" placeholder="滚木"></textarea>
    <button type="submit">提问</button>
  </form>
  <p v-if="error">{{ error }}</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const categories = ref([])
const categoryId = ref(null)
const title = ref('')
const content = ref('')
const error = ref('')

async function submit() {
  error.value = ''
  try {
    const { data } = await api.createQuestion({
      title: title.value,
      content: content.value,
      category_id: categoryId.value || null,
    })
    router.push({ name: 'question', params: { id: data.id } })
  } catch (e) {
    error.value = e.response?.data?.detail || '滚木'
  }
}

onMounted(async () => {
  const { data } = await api.listCategories()
  categories.value = data
})
</script>
