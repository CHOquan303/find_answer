import { createRouter, createWebHistory } from 'vue-router'

const TOKEN_KEY = 'fa_token'
const USER_KEY = 'fa_user'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/search', name: 'search', component: () => import('../views/SearchView.vue') },
  { path: '/questions/:id', name: 'question', component: () => import('../views/QuestionDetail.vue') },
  { path: '/ask', name: 'ask', component: () => import('../views/AskQuestion.vue'), meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
  { path: '/notifications', name: 'notifications', component: () => import('../views/NotificationsView.vue'), meta: { requiresAuth: true } },
  { path: '/admin', name: 'admin', component: () => import('../views/admin/AdminView.vue'), meta: { requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem(TOKEN_KEY)
  const user = JSON.parse(localStorage.getItem(USER_KEY) || 'null')

  if (to.meta.requiresAdmin && !(user && user.is_admin)) {
    return { name: 'home' }
  }
  if (to.meta.requiresAuth && !token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})

export default router
