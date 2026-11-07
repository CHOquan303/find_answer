import axios from 'axios'

const TOKEN_KEY = 'fa_token'
const USER_KEY = 'fa_user'

const http = axios.create({ baseURL: '/api' })

http.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export default {
  // auth
  register: (data) => http.post('/auth/register', data),
  login: (data) => http.post('/auth/login', data),
  me: () => http.get('/users/me'),

  // questions
  listQuestions: (params) => http.get('/questions', { params }),
  getQuestion: (id) => http.get(`/questions/${id}`),
  createQuestion: (data) => http.post('/questions', data),
  resolveQuestion: (id) => http.patch(`/questions/${id}/resolve`),

  // answers
  createAnswer: (qid, data) => http.post(`/questions/${qid}/answers`, data),
  acceptAnswer: (qid, aid) => http.patch(`/questions/${qid}/answers/${aid}/accept`),
  likeAnswer: (id) => http.post(`/answers/${id}/like`),
  reportAnswer: (id, data) => http.post(`/answers/${id}/report`, data),
  createReply: (id, data) => http.post(`/answers/${id}/replies`, data),

  // categories
  listCategories: () => http.get('/categories'),

  // search
  search: (q) => http.get('/search', { params: { q } }),

  // notifications
  listNotifications: () => http.get('/notifications'),
  readNotification: (id) => http.patch(`/notifications/${id}/read`),

  // admin
  uploadRoster: (file) => {
    const form = new FormData()
    form.append('file', file)
    return http.post('/admin/roster', form)
  },
  createCategory: (data) => http.post('/admin/categories', data),
  deleteCategory: (id) => http.delete(`/admin/categories/${id}`),
  deleteQuestion: (id) => http.delete(`/admin/questions/${id}`),
  deleteAnswer: (id) => http.delete(`/admin/answers/${id}`),
  listReports: () => http.get('/admin/reports'),
  reviewReport: (id, status) => http.patch(`/admin/reports/${id}`, { status }),
}
