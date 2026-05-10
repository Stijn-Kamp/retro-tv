<template>
  <div class="weather">
    <span class="location">{{ location }}</span>
    <span class="degrees">{{ temperature }}°</span>
    <i :class="`fas fa-${weatherIcon} weather-icon`"></i>
  </div>
</template>

<script setup>
const location = 'Praha'
const temperature = 18
const weatherIcon = 'sun'
</script>

<style scoped>
.weather {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}

.degrees {
  color: var(--primary-color);
}
</style>