<template>
  <div class="bottom-bar">
    <span class="title">NOW PLAYING</span>
    &nbsp;• Retro TV Channel
  </div>
</template>

<style scoped>
.bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 280px; /* same width as sidebar */
  height: 30px;
  background: var(--overlay-bg);
  color: white;
  display: flex;
  align-items: center;
  margin: 30px;
  margin-right: 80px;
  padding: 0 20px;
  z-index: 10;
  pointer-events: none;
}

.title {
  color: var(--primary-color);
  font-weight: bold;
  margin-right: 4px;
}
</style>