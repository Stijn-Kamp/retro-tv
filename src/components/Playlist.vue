<template>
  <div class="playlist">
    <div class="header">
      <span>Playlist</span>
    </div>
    <div
      v-for="({ song, type }, i) in windowed"
      :key="song?.yt_id || i"
      class="item"
      :class="type"
    >
      <div class="row">
        <span class="artist">{{ song?.artist }}</span>
        <span class="duration" v-if="type !== 'prev'">{{ song?.duration }}</span>
      </div>
      <div class="row">
        <span class="title">{{ song?.title }}</span>
        <i v-if="type === 'current'" class="fa-solid fa-chart-simple icon"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  queue:     { type: Array,  default: () => [] },
  prevCount: { type: Number, default: 2 },
  nextCount: { type: Number, default: 4 },
})

const windowed = computed(() => {
  const q = props.queue
  if (!q.length) return []

  const prevItems = Array.from({ length: props.prevCount }, (_, i) => ({
    song: q.at(-(props.prevCount - i)) ?? null,
    type: 'prev'
  }))

  const currentItem = { song: q[0] ?? null, type: 'current' }

  const nextItems = Array.from({ length: props.nextCount }, (_, i) => ({
    song: q[i + 1] ?? null,
    type: 'next'
  }))

  return [...prevItems, currentItem, ...nextItems].filter(({ song }) => song)
})
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
  padding-bottom: 6px;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.current {
  position: relative;
  color: var(--primary-color);
}

.current .artist,
.current .title,
.current .duration {
  color: var(--primary-color);
}

.current::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -6px;
  height: 2px;
  background: var(--primary-color);
  border-radius: 2px;
}

.prev {
  opacity: 0.5;
}
</style>