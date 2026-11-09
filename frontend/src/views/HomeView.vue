<template>
  <div class="home">
    <div class="title-row">
      <h2>问答</h2>
      <router-link to="/ask" class="btn btn-solid">提问</router-link>
    </div>

    <div class="stat-row">
      <span class="stat">共 {{ total }} 个问题</span>
      <div class="filters">
        <button :class="{ active: status === null }" @click="setStatus(null)">全部</button>
        <button :class="{ active: status === 'unresolved' }" @click="setStatus('unresolved')">未解决</button>
        <button :class="{ active: status === 'resolved' }" @click="setStatus('resolved')">已解决</button>
      </div>
    </div>

    <div class="list">
      <QuestionCard
        v-for="q in items"
        :key="q.id"
        :q="q"
        :category-name="catName(q.category_id)"
      />
    </div>
    <p v-if="!items.length" class="empty">滚木</p>

    <div class="pager">
      <button :disabled="page <= 1" @click="prev">上一页</button>
      <span>{{ page }}</span>
      <button :disabled="page >= totalPages" @click="next">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import QuestionCard from '../components/QuestionCard.vue'

const PAGE_SIZE = 20

const route = useRoute()

const categories = ref([])
const items = ref([])
const total = ref(0)
const page = ref(1)
const category = ref(route.query.category ? Number(route.query.category) : null)
const status = ref(null)

const totalPages = computed(() => Math.ceil(total.value / PAGE_SIZE))

function catName(id) {
  return categories.value.find((c) => c.id === id)?.name || ''
}

function setStatus(s) {
  status.value = s
}

async function load() {
  const { data } = await api.listQuestions({
    page: page.value,
    category: category.value,
    status: status.value,
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

watch([category, status], () => {
  page.value = 1
  load()
})

watch(
  () => route.query.category,
  (v) => {
    category.value = v ? Number(v) : null
  }
)

onMounted(async () => {
  const { data } = await api.listCategories()
  categories.value = data
  load()
})
</script>

<style scoped>
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.stat {
  font-size: 14px;
  color: #666;
}
.filters {
  display: flex;
  gap: 8px;
  overflow-x: auto;
}
.filters button {
  flex-shrink: 0;
  padding: 4px 12px;
}
.filters button.active {
  background: #333;
  color: #fff;
  border-color: #333;
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
</style>
