import { defineStore } from 'pinia'
import api from '../api'

const TOKEN_KEY = 'fa_token'
const USER_KEY = 'fa_user'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: JSON.parse(localStorage.getItem(USER_KEY) || 'null'),
  }),
  getters: {
    isLoggedIn: (s) => !!s.token,
    canAsk: (s) => !!s.user && (s.user.is_name_verified || s.user.is_full_verified || s.user.is_admin),
    canAnswer: (s) => !!s.user && (s.user.is_full_verified || s.user.is_admin),
    isAdmin: (s) => !!s.user && s.user.is_admin,
  },
  actions: {
    setAuth(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem(TOKEN_KEY, token)
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    },
    async login(username, password) {
      const res = await api.login({ username, password })
      const token = res.data.access_token
      localStorage.setItem(TOKEN_KEY, token) // 先写 token，供 api.me 的拦截器使用
      const me = await api.me()
      this.setAuth(token, me.data)
      return me.data
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },
  },
})
