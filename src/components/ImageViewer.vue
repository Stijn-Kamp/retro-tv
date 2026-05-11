<template>
  <div class="image-viewer">
    <img :src="src" class="image" />
  </div>
</template>

<script setup>
defineProps({
  src: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.image-viewer {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: black;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
}
</style>