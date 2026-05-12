<template>
  <div class="playlist">
    <div class="header">
      <span>Playlist</span>
    </div>

    <div
      v-for="(song, i) in windowed"
      :key="song?.yt_id || i"
      class="item"
      :class="getClass(i)"
    >
      <span class="artist">{{ song?.artist }}</span>
      <span class="title">{{ song?.title }}</span>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  queue: {
    type: Array,
    default: () => []
  }
})

const windowed = computed(() => {
  const q = props.queue

  const current = q[0] ?? null
  const next = q[1] ?? null
  const later = q[2] ?? null
  const prev = q[q.length - 1] ?? null
  const prevPrev = q[q.length - 2] ?? null

  return [
    prevPrev,
    prev,
    current,
    next,
    later
  ].filter(Boolean)
})

function getClass(i) {
  if (i < 2) return 'prev'
  if (i === 2) return 'current'
  return 'next'
}
</script>

<style scoped>
.playlist {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.item {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.current,
.current .artist,
.current .title {
  color: var(--primary-color);
}
</style>