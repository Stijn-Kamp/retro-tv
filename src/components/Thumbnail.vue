<template>
  <div class="thumbnail-wrapper">
    <img :src="src" class="thumbnail" />
  </div>
</template>

<script setup>
defineProps({
  src: String
})
</script>

<style scoped>
.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  flex-shrink: 0;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>