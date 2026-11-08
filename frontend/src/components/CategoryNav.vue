<template>
  <nav class="cats">
    <button @click="$emit('update:modelValue', null)">全部</button>
    <button
      v-for="c in categories"
      :key="c.id"
      @click="$emit('update:modelValue', c.id)"
    >
      {{ c.name }}
    </button>
  </nav>
</template>

<script setup>
defineProps({
  categories: { type: Array, default: () => [] },
  modelValue: { default: null },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.cats {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  margin-bottom: 12px;
}
.cats button {
  flex-shrink: 0;
  padding: 6px 12px;
}
</style>
