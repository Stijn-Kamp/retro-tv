<template>
  <span class="datetime">{{ datetime }}</span>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

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

onUnmounted(() => {
  clearInterval(interval)
})
</script>
