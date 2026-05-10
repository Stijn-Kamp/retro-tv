<template>
  <div class="bottom-bar overlay-bar">
    <span class="title">{{ title }}</span>
    <span class="message">{{ message }}</span>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  message: String
})
</script>

<style scoped>
.bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 280px;
  height: 30px;
  display: flex;
  align-items: center;
  margin: 30px;
  margin-right: 80px;
  padding: 0 20px;
  gap: 16px;
}

.title {
  color: var(--primary-color);
  font-weight: bold;
}
</style>