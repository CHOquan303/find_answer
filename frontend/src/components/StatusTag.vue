<template>
  <span class="tag">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ status: { type: String, required: true } })

const label = computed(() => {
  const map = { pending: '待回答', answered: '已回答', resolved: '已解决' }
  return map[props.status] || '滚木'
})
</script>
