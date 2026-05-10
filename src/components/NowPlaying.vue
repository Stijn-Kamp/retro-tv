<template>
  <div class="now-playing">
    <div class="year-row">
      <span class="year">'{{ year }}</span>
      <span class="datetime">{{ datetime }}</span>
    </div>
    <p class="artist">{{ artist }}</p>
    <p class="detail">
      <i class="fas fa-music"></i>
      {{ song }}
    </p>
    <p class="detail">
      <i class="fas fa-compact-disc"></i>
      {{ album }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

defineProps({
  artist: String,
  song: String,
  album: String,
  year: String
})

const datetime = ref('')

const updateTime = () => {
  datetime.value = new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}
let interval
onMounted(() => {
  updateTime()
  interval = setInterval(updateTime, 1000)
})
onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.now-playing {
  padding: 8px 20px 16px;
  flex-shrink: 0;
}

.year-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 8px;
}

.year {
  font-size: 1.6rem;
  font-weight: bold;
  color: var(--primary-color);
}

.datetime {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

.artist {
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
  margin: 0 0 10px;
}

.detail {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.85);
  margin: 0 0 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail i {
  color: var(--primary-color);
  width: 14px;
  text-align: center;
}
</style>