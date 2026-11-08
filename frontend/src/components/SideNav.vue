<template>
  <div v-if="open" class="drawer-mask" @click="$emit('close')"></div>
  <nav class="side-nav" :class="{ open }">
    <button class="side-item" :class="{ active: !categoryId }" @click="go(null)">全部</button>
    <button
      v-for="c in categories"
      :key="c.id"
      class="side-item"
      :class="{ active: categoryId === c.id }"
      @click="go(c.id)"
    >
      {{ c.name }}
    </button>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

defineProps({ open: { type: Boolean, default: false } })
const emit = defineEmits(['close'])

const route = useRoute()
const router = useRouter()
const categories = ref([])

const categoryId = computed(() => {
  const v = route.query.category
  return v ? Number(v) : null
})

function go(id) {
  router.push({ name: 'home', query: id ? { category: id } : {} })
  emit('close')
}

onMounted(async () => {
  const { data } = await api.listCategories()
  categories.value = data
})
</script>

<style scoped>
.side-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.side-item {
  text-align: left;
  border: none;
  background: none;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 15px;
}
.side-item.active {
  background: #eee;
  font-weight: bold;
}
.drawer-mask {
  display: none;
}
@media (max-width: 959px) {
  .side-nav {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 220px;
    background: #fff;
    padding: 16px;
    z-index: 200;
    transform: translateX(-100%);
    transition: transform 0.2s;
  }
  .side-nav.open {
    transform: translateX(0);
  }
  .drawer-mask {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 199;
  }
}
</style>
