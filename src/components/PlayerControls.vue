<template>
  <div class="player-controls overlay-bar">
    <button @click="emit('prev')">
      <i class="fas fa-backward-step"></i>
    </button>
    <button @click="emit('toggle-pause')">
      <i :class="paused ? 'fas fa-play' : 'fas fa-pause'"></i>
    </button>
    <button @click="emit('skip')">
      <i class="fas fa-forward-step"></i>
    </button>
    <button @click="emit('reshuffle')">
      <i class="fas fa-shuffle"></i>
    </button>
  </div>
</template>

<script setup>
defineProps({ paused: Boolean })
const emit = defineEmits(['prev', 'toggle-pause', 'skip', 'reshuffle'])
</script>

<style scoped>
.player-controls {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  pointer-events: all;
}

button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color);
  font-size: 1.4rem;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  border-radius: 50%;
  justify-content: center;
  transition: color 0.15s, background 0.15s;
}

button:hover {
  color: var(--primary-color);
  background: rgba(29, 221, 242, 0.1);
}

button:active {
  color: var(--primary-color);
  background: rgba(29, 221, 242, 0.2);
}
</style>