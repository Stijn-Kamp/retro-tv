<template>
  <div class="right-sidebar">
    <h3>Playlist</h3>
    <ul>
      <li>Black Eyed Peas - Pump It</li>
      <li>Snap! - Rhythm Is a Dancer</li>
      <li>Daft Punk - Around the World</li>
    </ul>
  </div>
</template>

<style scoped>
.right-sidebar {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  background: var(--overlay-bg);
  color: white;
  padding: 20px;
  z-index: 10;
  pointer-events: none;
}
</style>