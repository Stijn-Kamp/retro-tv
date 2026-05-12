<template>
  <div class="rotating-panel info-overlay">
    <Transition name="slide-fade" mode="out-in">
      <CurrentTime v-if="showTime" key="time" />
      <CurrentWeather v-else key="weather" />
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import CurrentTime from './CurrentTime.vue'
import CurrentWeather from './CurrentWeather.vue'

const showTime = ref(true)

let interval

onMounted(() => {
  interval = setInterval(() => {
    showTime.value = !showTime.value
  }, 30000)
})

onUnmounted(() => clearInterval(interval))
</script>

<style>
.info-overlay {
  position: absolute;
  padding: 1em;
  z-index: 20;
  top: 25px;
  right: 30px;
  font-size: 1.5em;;
}
</style>