<template>
  <form @submit.prevent="submit">
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" type="password" placeholder="密码" />
    <input v-model="realName" placeholder="真实姓名" />
    <input v-model="studentId" placeholder="学号（可选）" />
    <select v-model="grade">
      <option value="">滚木（年级可选）</option>
      <option value="freshman">大一</option>
      <option value="sophomore">大二</option>
      <option value="junior">大三</option>
      <option value="senior">大四</option>
    </select>
    <button type="submit">注册</button>
  </form>
  <p v-if="error">{{ error }}</p>
  <p v-if="result">{{ result.verify_hint }}</p>
  <router-link to="/login">登录</router-link>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const username = ref('')
const password = ref('')
const realName = ref('')
const studentId = ref('')
const grade = ref('')
const error = ref('')
const result = ref(null)

async function submit() {
  error.value = ''
  result.value = null
  try {
    const { data } = await api.register({
      username: username.value,
      password: password.value,
      real_name: realName.value,
      student_id: studentId.value || null,
      grade: grade.value || null,
    })
    result.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || '滚木'
  }
}
</script>
