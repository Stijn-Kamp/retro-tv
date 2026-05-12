<template>
  <div class="bottom-bar overlay-bar">
    <Transition name="slide-fade" mode="out-in">
      <div class="item" :key="currentIndex">
        <span class="title">{{ currentItem.title }}</span>
        <span class="message">{{ currentItem.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  interval: {
    type: Number,
    default: 10000
  }
})

const currentIndex = ref(0)

const currentItem = computed(() => {
  return props.items.length
    ? props.items[currentIndex.value]
    : { title: '', message: '' }
})

let timer

onMounted(() => {
  if (props.items.length <= 1) return

  timer = setInterval(() => {
    currentIndex.value =
      (currentIndex.value + 1) % props.items.length
  }, props.interval)
})

onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 390px;
  height: 30px;
  display: flex;
  align-items: center;
  margin: 30px;
  margin-right: 80px;
  padding: 0 20px;
  gap: 16px;
  overflow: hidden;
}

.item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title {
  color: var(--primary-color);
  font-weight: bold;
}
</style>