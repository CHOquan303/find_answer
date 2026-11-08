<template>
  <div class="container">
    <section class="card">
      <h3>滚木（名单）</h3>
      <input type="file" @change="onFile" />
      <p v-if="imported !== null">已导入 {{ imported }} 条</p>
    </section>

    <section class="card">
      <h3>滚木（分类）</h3>
      <div class="row">
        <input v-model="categoryName" placeholder="分类名" />
        <button @click="addCategory">新增分类</button>
      </div>
      <div v-for="c in categories" :key="c.id" class="row">
        <span>{{ c.name }}</span>
        <button @click="removeCategory(c.id)">删除</button>
      </div>
    </section>

    <section class="card">
      <h3>滚木（举报审核）</h3>
      <div v-for="r in reports" :key="r.id" class="report">
        <span>回答#{{ r.answer_id }} · {{ r.reason }} · {{ r.status }}</span>
        <button v-if="r.status === 'pending'" @click="review(r.id, 'confirmed')">确认</button>
        <button v-if="r.status === 'pending'" @click="review(r.id, 'dismissed')">驳回</button>
      </div>
    </section>

    <section class="card">
      <h3>滚木（违规删除）</h3>
      <div class="row">
        <input v-model.number="delId" placeholder="问题/回答 ID" />
        <button @click="delQuestion">删问题</button>
        <button @click="delAnswer">删回答</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const imported = ref(null)
const categories = ref([])
const reports = ref([])
const categoryName = ref('')
const delId = ref(null)

async function onFile(e) {
  const file = e.target.files[0]
  if (!file) return
  const { data } = await api.uploadRoster(file)
  imported.value = data.imported
}

async function loadCategories() {
  const { data } = await api.listCategories()
  categories.value = data
}

async function addCategory() {
  const name = categoryName.value.trim()
  if (!name) return
  await api.createCategory({ name })
  categoryName.value = ''
  loadCategories()
}

async function removeCategory(id) {
  await api.deleteCategory(id)
  loadCategories()
}

async function loadReports() {
  const { data } = await api.listReports()
  reports.value = data
}

async function review(id, status) {
  await api.reviewReport(id, status)
  loadReports()
}

async function delQuestion() {
  if (!delId.value) return
  await api.deleteQuestion(delId.value)
  delId.value = null
}

async function delAnswer() {
  if (!delId.value) return
  await api.deleteAnswer(delId.value)
  delId.value = null
}

onMounted(() => {
  loadCategories()
  loadReports()
})
</script>

<style scoped>
.row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 8px;
}
.row input {
  flex: 1;
  width: auto;
}
.report {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 8px;
}
</style>
