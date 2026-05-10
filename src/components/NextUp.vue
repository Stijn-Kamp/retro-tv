<template>
  <div class="next-up">
    <p class="label">Next</p>
    <p class="song">{{ song }}</p>
  </div>
</template>

<script setup>
defineProps({
  song: String
})
</script>

<style scoped>
.next-up {
  padding: 16px 20px 8px;
  flex-shrink: 0;
}

.label {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  margin: 0 0 6px;
}

.song {
  font-size: 1rem;
  color: white;
  margin: 0;
}
</style>