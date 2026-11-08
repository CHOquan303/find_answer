<template>
  <div class="container">
    <SearchBar />
    <CategoryNav v-model="category" :categories="categories" />
    <div class="toolbar">
      <select v-model="sort">
        <option value="latest">最新</option>
        <option value="hot">热门</option>
      </select>
    </div>

    <div v-for="q in items" :key="q.id">
      <QuestionCard :q="q" />
    </div>
    <p v-if="!items.length" class="empty">滚木</p>

    <div class="pager">
      <button :disabled="page <= 1" @click="prev">上一页</button>
      <span>{{ page }}</span>
      <button @click="next">下一页</button>
    </div>
  </div>

  <router-link class="ask-fab" to="/ask">提问</router-link>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api'
import SearchBar from '../components/SearchBar.vue'
import CategoryNav from '../components/CategoryNav.vue'
import QuestionCard from '../components/QuestionCard.vue'

const categories = ref([])
const items = ref([])
const total = ref(0)
const page = ref(1)
const category = ref(null)
const sort = ref('latest')

async function load() {
  const { data } = await api.listQuestions({
    page: page.value,
    category: category.value,
    sort: sort.value,
  })
  items.value = data.items
  total.value = data.total
}

function prev() {
  if (page.value > 1) {
    page.value--
    load()
  }
}

function next() {
  page.value++
  load()
}

watch([category, sort], () => {
  page.value = 1
  load()
})

onMounted(async () => {
  const { data } = await api.listCategories()
  categories.value = data
  load()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 12px;
}
.toolbar select {
  width: auto;
}
.empty {
  text-align: center;
  color: #999;
  padding: 24px 0;
}
.pager {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}
.ask-fab {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: #fff;
  padding: 12px 24px;
  border-radius: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>
