<template>
  <span class="tag">{{ title || '滚木' }}</span>
</template>

<script setup>
defineProps({ title: { type: String, default: '' } })
</script>
