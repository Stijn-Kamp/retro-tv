<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  src: String
})

const loaded = ref(false)

function checkImage(src) {
  if (!src) {
    loaded.value = false
    return
  }

  const img = new Image()
  img.src = src

  img.onload = () => {
    loaded.value = true
  }

  img.onerror = () => {
    loaded.value = false
  }
}

watch(() => props.src, checkImage, { immediate: true })
</script>

<template>
  <div v-if="loaded" class="thumbnail-wrapper">
    <img :src="src" class="thumbnail" />
  </div>
</template>

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