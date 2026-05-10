<template>
  <div class="rotating-panel">
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