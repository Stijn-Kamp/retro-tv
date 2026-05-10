<template>
  <div class="now-playing">
    <div class="year-row">
      <span class="year">'{{ year }}</span>
      <InfoComponent />
    </div>

    <p class="artist" v-if="artist">{{ artist }}</p>

    <div class="details">
      <p class="detail" v-if="song">
        <i class="fas fa-music"></i>
        {{ song }}
      </p>

      <p class="detail" v-if="album">
        <i class="fas fa-compact-disc"></i>
        {{ album }}
      </p>

      <p class="detail" v-if="info">
        <i class="fas fa-circle-info"></i>
        {{ info }}
      </p>
    </div>
  </div>
</template>

<script setup>
import InfoComponent from './InfoComponent.vue';

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

.artist {
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
  margin: 0 0 10px;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 8px;
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