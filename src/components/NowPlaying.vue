<template>
  <div class="now-playing">
    <div class="year-row">
      <span class="header">'{{ song?.year }}</span>
    </div>

    <p class="artist" v-if="song?.artist">
      {{ song.artist }}
    </p>

    <div class="details">
      <p class="detail" v-if="song?.title">
        <i class="fas fa-music"></i>
        {{ song.title }}
      </p>

      <p class="detail" v-if="song?.album">
        <i class="fas fa-compact-disc"></i>
        {{ song.album }}
      </p>

      <p class="detail" v-if="song?.info">
        <i class="fas fa-circle-info"></i>
        {{ song.info }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  artist: String,
  song: String,
  album: String,
  year: String,
  info: String
})
</script>

<style scoped>
.now-playing {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.year-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  width: 100%;
}

.artist {
  font-size: 1.2em;
  font-weight: bold;
  color: white;
  margin: 0 0 10px;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail {
  color: rgba(255, 255, 255, 0.85);
  margin: 0 0 6px;
  display: flex;
  align-items: center;
  gap: 1em;
}

.detail i {
  color: var(--primary-color);
  width: 14px;
  text-align: center;
}
</style>