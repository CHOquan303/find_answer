<template>
  <header class="top-nav">
    <div class="top-inner">
      <button class="hamburger" aria-label="打开菜单" @click="$emit('toggle-nav')">☰</button>
      <router-link to="/" class="brand">滚木</router-link>
      <div class="search-slot">
        <SearchBar />
      </div>
      <div class="auth">
        <template v-if="!auth.isLoggedIn">
          <router-link to="/login" class="btn btn-outline">登录</router-link>
          <router-link to="/register" class="btn btn-solid">注册</router-link>
        </template>
        <template v-else>
          <router-link to="/notifications" class="user">{{ auth.user?.username }}</router-link>
          <button class="btn btn-outline" @click="logout">退出</button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import SearchBar from './SearchBar.vue'

defineEmits(['toggle-nav'])

const router = useRouter()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid #ddd;
}
.top-inner {
  max-width: 1080px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
}
.hamburger {
  display: none;
  border: none;
  background: none;
  font-size: 20px;
  padding: 4px 8px;
}
.brand {
  font-size: 18px;
  font-weight: bold;
  flex-shrink: 0;
}
.search-slot {
  flex: 1;
  display: flex;
  justify-content: center;
}
.search-slot :deep(.search) {
  width: 100%;
  max-width: 420px;
}
.auth {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}
.user {
  color: #333;
}
@media (max-width: 959px) {
  .hamburger {
    display: block;
  }
}
</style>
