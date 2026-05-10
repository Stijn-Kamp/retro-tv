<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  paused: { type: Boolean, default: false },
})
const emit = defineEmits(['ended'])
const videoEl = ref(null)

let userHasInteracted = false

onMounted(() => {
  document.addEventListener('click', () => {
    userHasInteracted = true
    if (videoEl.value) videoEl.value.muted = false
  }, { once: true })
})

watch(() => props.src, async () => {
  if (!videoEl.value) return
  
  // Don't call load() — just update src and play directly
  videoEl.value.src = props.src
  videoEl.value.muted = !userHasInteracted

  try {
    await videoEl.value.play()
    console.log('playing — muted:', videoEl.value.muted)
  } catch (e) {
    console.warn('play failed:', e)
  }
}, { immediate: true })

watch(() => props.paused, (isPaused) => {
  if (!videoEl.value) return
  isPaused ? videoEl.value.pause() : videoEl.value.play()
})
</script>

<template>
  <div class="video-container">
    <video
      ref="videoEl"
      autoplay
      @ended="emit('ended')"
      class="video-element"
    />
  </div>
</template>

<style scoped>
.video-container {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: black;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>