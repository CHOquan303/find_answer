<template>
  <div class="item" @click="go">
    <div class="counts">
      <div class="count">
        <span class="num">{{ q.answer_count }}</span>
        <span class="label">回答</span>
      </div>
      <div class="count">
        <span class="num">滚木</span>
        <span class="label">浏览</span>
      </div>
    </div>
    <div class="body">
      <h3 class="title">{{ q.title }}</h3>
      <p class="excerpt">{{ excerpt }}</p>
      <div class="tags">
        <StatusTag :status="q.status" />
        <span v-if="categoryName" class="tag">{{ categoryName }}</span>
      </div>
      <div class="meta">{{ authorName }} · {{ time }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import StatusTag from './StatusTag.vue'

const props = defineProps({
  q: { type: Object, required: true },
  categoryName: { type: String, default: '' },
})
const router = useRouter()

const excerpt = computed(() => {
  const c = (props.q.content || '').replace(/\s+/g, ' ')
  return c.length > 60 ? c.slice(0, 60) + '…' : c
})
const authorName = computed(
  () => props.q.author?.real_name || props.q.author?.username || '滚木'
)
const time = computed(() => (props.q.created_at || '').slice(0, 10))

function go() {
  router.push({ name: 'question', params: { id: props.q.id } })
}
</script>

<style scoped>
.item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}
.counts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  min-width: 56px;
}
.count {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.num {
  font-size: 16px;
  font-variant-numeric: tabular-nums;
}
.label {
  font-size: 12px;
  color: #999;
}
.body {
  flex: 1;
  min-width: 0;
}
.title {
  margin-bottom: 4px;
}
.excerpt {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}
.tags {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}
.meta {
  font-size: 13px;
  color: #999;
  text-align: right;
}
</style>
